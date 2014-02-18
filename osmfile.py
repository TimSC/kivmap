
import os
import trianglecollision
import xml.parsers.expat as expat
from xml.sax.saxutils import escape, quoteattr
from pyshull.earclipping import EarClipping
import slippy

try:
	import bz2
	bz2Available = True
except:
	bz2Available = False
try:
	import gzip
	gzipAvailable = True
except:
	gzipAvailable = False
try:
	import zipfile
	zipAvailable = True
except:
	zipAvailable = False


def GetNodesFromWay(nodeIdList, osmParseObj):
	wayNodes = []

	for ntag, nid in nodeIdList:
		nidInt = int(nid['ref'])

		if nidInt not in osmParseObj.nodes:
			wayNodes.append((nidInt, None, None, None))
			continue

		nodeObj = osmParseObj.nodes[nidInt]	
		nodeAttrs = nodeObj[0]
		nodeTags = nodeObj[1]
		nodeLat = float(nodeAttrs['lat'])
		nodeLon = float(nodeAttrs['lon'])
	
		wayNodes.append((nidInt, (nodeLat, nodeLon), nodeAttrs, nodeTags))

	return wayNodes

def GetNodesFromWayId(wayId, osmParseObj):
	wayNodes = []

	if wayId not in osmParseObj.ways:
		return None
	way = osmParseObj.ways[wayId]

	for ntag, nid in way[2]:
		nidInt = int(nid['ref'])

		if nidInt not in osmParseObj.nodes:
			wayNodes.append((nidInt, None, None, None))
			continue

		nodeObj = osmParseObj.nodes[nidInt]	
		nodeAttrs = nodeObj[0]
		nodeTags = nodeObj[1]
		nodeLat = float(nodeAttrs['lat'])
		nodeLon = float(nodeAttrs['lon'])
	
		wayNodes.append((nidInt, (nodeLat, nodeLon), nodeAttrs, nodeTags))

	return wayNodes

def WayNodesInRoi(wayNodes, bounds):
	wayInRoi = False
	for node in wayNodes:
		if node[1] is None:
			continue

		if wayInRoi is False and bounds is not None and \
			node[1][0] >= bounds[1] and node[1][0] < bounds[3] and \
			node[1][1] >= bounds[0] and node[1][1] < bounds[2]: 
				
			wayInRoi = True	
	return wayInRoi

def MergeWayFragments(wayData):
	#print "MergeWayFragments", len(wayData)
	i = 0
	wayData = wayData[:] #Get copy for modification

	while i < len(wayData):
		way, closed = wayData[i]

		if closed:
			i+=1
			continue

		firstNodeId = way[0][0]
		lastNodeId = way[-1][0]
		j = 0

		while j < len(wayData):
			if i >= j: 
				j+=1
				continue #Don't merge with self
			way2, closed2 = wayData[j]

			if closed2:
				j+=1
				continue

			chkFirstNodeId = way2[0][0]
			chkLastNodeId = way2[-1][0]
			
			if firstNodeId == chkFirstNodeId:
				#print "Merging1"
				combinedWay = way2[:1:-1]
				combinedWay.extend(way[:])
				closed = chkLastNodeId == lastNodeId
				wayData[i] = (combinedWay, closed)
				del wayData[j]
				j = 0
				continue

			if firstNodeId == chkLastNodeId:
				#print "Merging2"
				combinedWay = way2[:]
				combinedWay.extend(way[1:])
				closed = chkFirstNodeId == lastNodeId
				wayData[i] = (combinedWay, closed)
				del wayData[j]
				j = 0
				continue

			if lastNodeId == chkFirstNodeId:
				#print "Merging3"
				combinedWay = way[:]
				combinedWay.extend(way2[1:])
				closed = chkLastNodeId == firstNodeId
				wayData[i] = (combinedWay, closed)
				del wayData[j]
				j = 0
				continue

			if lastNodeId == chkLastNodeId:
				#print "Merging4"
				combinedWay = way[:]
				combinedWay.extend(way2[:1:-1])
				closed = chkFirstNodeId == firstNodeId
				wayData[i] = (combinedWay, closed)
				del wayData[j]
				j = 0
				continue

			j += 1

		i += 1

	return wayData

def ProcessMultipoly(outerWays, innerWays):
	#Match corresponding outer and inner ways
	outerWaysData = [way[0] for way in outerWays]
	innerWaysData = [way[0] for way in innerWays]
	outerWaysTri = []
	innerWaysTri = []

	for outerWayData in outerWaysData:
		nodePoss = IgnoreNull(ExtractLatLon(outerWayData))

		pts, triangles = EarClipping(nodePoss)
		outerWaysTri.append((pts, triangles))

	for innerWayData in innerWaysData:
		nodePoss = IgnoreNull(ExtractLatLon(innerWayData))

		pts, triangles = EarClipping(nodePoss)
		innerWaysTri.append((pts, triangles))

	innerWaysInOuterNum = []
	for oNum, outerWayTri in enumerate(outerWaysTri):
		matchIndices = []
		for iNum, innerWayTri in enumerate(innerWaysTri):
			coll = trianglecollision.DoPolyPolyCollision(outerWayTri[0], outerWayTri[1], 
				innerWayTri[0], innerWayTri[1])
			if coll:
				matchIndices.append(iNum)
		innerWaysInOuterNum.append(matchIndices)
	
	#print len(outerWays), len(innerWays)
	#print innerWaysInOuterNum

	#Group outer and corresponding inner ways
	out = []
	for i, ow in enumerate(outerWays):
		containedWays = innerWaysInOuterNum[i]
		iws = []
		for iw in containedWays:
			iws.append(innerWays[iw][0])
		out.append([ow[0], iws])

	return out

def IgnoreNull(nodes):
	filteredNodes = []
	for n in nodes:	
		if n is not None:
			filteredNodes.append(n)
	return filteredNodes

def ExtractLatLon(nodes):
	return [p[1] for p in nodes]

class OsmObjToLinesAndPolys(object):
	def __init__(self):
		self.tagsOfInterest = {}
		self.closeWaysAreAreas = True

	def AddTagOfInterest(self, key, val="*", area = None):
		if key not in self.tagsOfInterest:
			self.tagsOfInterest[key] = []
		self.tagsOfInterest[key].append((val, area))

	def Do(self, osmParseObj, tileCode, tileZoom):

		tl = slippy.num2deg(tileCode[0], tileCode[1], tileZoom)
		#tileResolution = 512
		br = slippy.num2deg(tileCode[0]+1, tileCode[1]+1, tileZoom)
		#proj = slippy.TileProj(tileCode[0], tileCode[1], tileZoom, tileResolution, tileResolution)
		bounds = (tl[1], br[0], br[1], tl[0])

		wayLines = []
		for objId in osmParseObj.ways:
			w = osmParseObj.ways[objId]
			tags = w[1]
			isArea = None
			foundAreaVal = None
			ofInterest = False
			
			for tagOfInterest in self.tagsOfInterest:
				if tagOfInterest in tags:
					searchVal = self.tagsOfInterest[tagOfInterest]

					for val, valArea in searchVal:
						if "*" == val:
							ofInterest = True
							foundAreaVal = valArea
						if tags[tagOfInterest] == val:
							ofInterest = True
							foundAreaVal = valArea

			if not ofInterest:
				continue

			firstNode = w[2][0][1]
			lastNode = w[2][-1][1]

			if 'area' in tags:
				areaValue = str(tags['area'])
				if areaValue.lower() in ["yes", "1"]:
					isArea = True
				if areaValue.lower() in ["no", "0"]:
					isArea = False

			if isArea is None and foundAreaVal is not None:
				isArea = foundAreaVal

			if isArea is None and self.closeWaysAreAreas and int(firstNode['ref']) == int(lastNode['ref']):
				isArea = True

			if isArea is None:
				isArea = False #Default to unclosed

			wayNodes = GetNodesFromWay(w[2], osmParseObj)

			wayInRoi = WayNodesInRoi(wayNodes, bounds)
			
			#print objId, tags, w[2], wayNodes

			if wayInRoi or bounds is None:
				if isArea:
					nodes = wayNodes[:-1]
					filteredNodes = IgnoreNull(ExtractLatLon(nodes))

					try:
						pts, triangles = EarClipping(filteredNodes)
					except Exception as err:
						print "EarClipping error:", err
						continue

					wayLines.append(('tripoly', objId, tags, (pts, triangles, ("wgs84",))))
				else:
					wayLines.append(('line', objId, tags, wayNodes))

		#Convert relations to multipolygons
		for objId in osmParseObj.relations:
			w = osmParseObj.relations[objId]
			tags = w[1]
			innerWays = []
			outerWays = []
			checkWayInRoi = False

			if 'type' in tags:
				if  tags['type'] != "multipolygon":
					continue
			else:
				continue
			
			innerWayMembers = []
			outerWayMembers = []

			for mem, memData in w[2]:
				role = None
				if "role" in memData:
					role = memData['role']

				if role == "inner":
					innerWayMembers.append((mem, memData))
				if role == "outer":
					outerWayMembers.append((mem, memData))

			for mem, memData in outerWayMembers:
				wayId = int(memData['ref'])
				wayShape = GetNodesFromWayId(wayId, osmParseObj)
				if wayShape is None: continue #Way not found
				wayInRoi = WayNodesInRoi(wayShape, bounds)
				if wayInRoi:
					checkWayInRoi = True

				if len(wayShape) == 0:
					continue #Ignore ways when empty or all nodes are missing
				firstNodeId = wayShape[0][0]
				lastNodeId = wayShape[-1][0]
				if firstNodeId != lastNodeId:
					outerWays.append((wayShape, 0))
				else:
					outerWays.append((wayShape[:-1], 1))

			if checkWayInRoi is False:
				continue

			for mem, memData in innerWayMembers:
				wayId = int(memData['ref'])
				wayShape = GetNodesFromWayId(wayId, osmParseObj)
				if wayShape is None: continue #Way not found
				wayInRoi = WayNodesInRoi(wayShape, bounds)
				if wayInRoi:
					checkWayInRoi = True

				if len(wayShape) == 0:
					continue #Ignore ways when empty or all nodes are missing
				firstNodeId = wayShape[0][0]
				lastNodeId = wayShape[-1][0]
				if firstNodeId != lastNodeId:
					innerWays.append((wayShape, 0))
				else:
					innerWays.append((wayShape[:-1], 1))

			#Join unclosed ways to form more complete ways, if possible
			#for ow, clo in outerWays:
			#	print "frag", ow[0][0], ow[-1][0]
			preMergeCount = len(outerWays)
			outerWays = MergeWayFragments(outerWays)
			#if len(outerWays) != preMergeCount:
			#	print "result of merge", len(outerWays), preMergeCount
			for ow, clo in outerWays:
				if clo is False:
					print "Warning: unclosed outer way", ow[0][0], ow[-1][0]

			innerWays = MergeWayFragments(innerWays)
			for ow, clo in innerWays:
				if clo is False:
					print "Warning: unclosed inner way", ow[0][0], ow[-1][0]

	
			#print "tags", tags
			#print "inner", innerWays
			#print "outer", outerWays

			#if checkWayInRoi is False:
			#	continue

			#If there are multiple outer ways, sort into separate multipolygons
			if len(outerWays) > 0:
				if len(innerWays) > 0:
					#print "Outer polygons with inner ways", objId
					groupedPolys = ProcessMultipoly(outerWays, innerWays)
					if len(groupedPolys) > 0:
						wayLines.append(('multipoly', objId, tags, groupedPolys))
				else:
					#One or more outer ways and no inner ways
					outerWayData = [way[0] for way in outerWays]
					shapes = [[way, []] for way in outerWayData]

					for shape in shapes:
						try:
							o = IgnoreNull(ExtractLatLon(shape[0]))
							ins = map(IgnoreNull, map(ExtractLatLon, shape[1]))
							pts, triangles = EarClipping(o, ins)
						except Exception as err:
							print "EarClipping error in multipoly:", err
							continue

						wayLines.append(('tripoly', objId, tags, (pts, triangles)))
	
			if len(outerWays) == 0: #Ignore shape if no outer way exists
				continue


		return wayLines

class OsmParse(object):
	def __init__(self):
		self.parser = expat.ParserCreate()
		self.parser.CharacterDataHandler = self.HandleCharData
		self.parser.StartElementHandler = self.HandleStartElement
		self.parser.EndElementHandler = self.HandleEndElement
		self.depth = 0
		self.tags = []
		self.attr = []
		self.objectTags = {}
		self.objectMembers = []
		self.nodes = {}
		self.ways = {}
		self.relations = {}

	def ParseFile(self, fi):
		self.fiTmp = fi
		self.parser.ParseFile(fi)

	def HandleCharData(self, data):
		pass

	def HandleStartElement(self, name, attrs):
		self.depth += 1
		self.tags.append(name)
		self.attr.append(attrs)

		if self.depth == 2:
			self.objectTags = {}
			self.objectMembers = []

		if self.depth == 3:
			if name == "tag":
				self.objectTags[attrs['k']] = attrs['v']
			else:
				self.objectMembers.append((name, attrs))

	def HandleEndElement(self, name): 
		if self.depth == 2:
			#At this point, the entire object is available, inc tags and members
			objAttr = self.attr[-1]
			objId = int(objAttr['id'])
			#print name, objAttr, self.objectTags, self.objectMembers
			if name == "node":
				self.nodes[objId] = (objAttr, self.objectTags, self.objectMembers)
			if name == "way":
				self.ways[objId] = (objAttr, self.objectTags, self.objectMembers)
			if name == "relation":
				self.relations[objId] = (objAttr, self.objectTags, self.objectMembers)

		self.depth -= 1
		self.tags.pop()
		self.attr.pop()

class OsmFile(object):
	def __init__(self, fina):
		fi = None
		finaSplit = os.path.splitext(fina)
		if bz2Available and finaSplit[1] == ".bz2":
			fi = bz2.BZ2File(fina)
		if gzipAvailable and finaSplit[1] == ".gz":
			fi = gzip.GzipFile(fina)
		if zipAvailable and finaSplit[1] == ".zip":
			fi = zipfile.ZipFile(fina)

		if finaSplit[1] == ".osm":
			fi = open(fina, "rt")
		if fi is None:
			raise Exception ("Unknown file extension "+str(finaSplit[1]))
		
		self.osmParse = OsmParse()
		self.osmParse.ParseFile(fi)

		print "Read {0} nodes, {1} ways, {2} relations".format(len(self.osmParse.nodes),
			len(self.osmParse.ways),
			len(self.osmParse.relations))

	def GetHighwayNetwork(self, tileCode=None, tileZoom=12, hints={}):

		osmObjToLinesAndPolys = OsmObjToLinesAndPolys()
		osmObjToLinesAndPolys.AddTagOfInterest('highway',"*")
		shapes = osmObjToLinesAndPolys.Do(self.osmParse, tileCode, tileZoom)
		return shapes

	def GetRailNetwork(self, tileCode=None, hints={}):
		pass

	def GetWater(self, tileCode=None, tileZoom=12, hints={}):
		osmObjToLinesAndPolys = OsmObjToLinesAndPolys()
		osmObjToLinesAndPolys.AddTagOfInterest('waterway',"*")
		osmObjToLinesAndPolys.AddTagOfInterest('water',"*")
		osmObjToLinesAndPolys.AddTagOfInterest('natural',"coastline", 0)
		shapes = osmObjToLinesAndPolys.Do(self.osmParse, tileCode, tileZoom)
		return shapes

	def GetLandscape(self, tileCode=None, tileZoom=12, hints={}):
		osmObjToLinesAndPolys = OsmObjToLinesAndPolys()
		osmObjToLinesAndPolys.AddTagOfInterest('landuse',"*")
		osmObjToLinesAndPolys.AddTagOfInterest('natural',"wood")
		shapes = osmObjToLinesAndPolys.Do(self.osmParse, tileCode, tileZoom)
		return shapes

	def GetContours(self, tileCode=None, tileZoom=12, hints={}):
		pass

	def GetInfrastructure(self, tileCode=None, tileZoom=12, hints={}):
		pass


if __name__ == "__main__":
	
	f = OsmFile("IsleOfWight-Fosm-Oct2013.osm.bz2")
	print len(f.GetHighwayNetwork())

