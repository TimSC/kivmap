
import bz2, os
import xml.parsers.expat as expat
from xml.sax.saxutils import escape, quoteattr

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

class OsmObjToLinesAndPolys(object):
	def __init__(self):
		self.tagsOfInterest = {}
		self.closeWaysAreAreas = True

	def AddTagOfInterest(self, key, val="*"):
		if key not in self.tagsOfInterest:
			self.tagsOfInterest[key] = []
		self.tagsOfInterest[key].append(val)

	def Do(self, osmParseObj, bounds = None):

		wayLines = []
		for objId in osmParseObj.ways:
			w = osmParseObj.ways[objId]
			tags = w[1]
			isArea = False
			ofInterest = False
			
			for tagOfInterest in self.tagsOfInterest:
				if tagOfInterest in tags:
					searchVal = self.tagsOfInterest[tagOfInterest]
					if "*" in searchVal:
						ofInterest = True
					if tags[tagOfInterest] in searchVal:
						ofInterest = True

			if not ofInterest:
				continue

			firstNode = w[2][0][1]
			lastNode = w[2][-1][1]

			if self.closeWaysAreAreas and int(firstNode['ref']) == int(lastNode['ref']):
				isArea = True

			if 'area' in tags:
				areaValue = str(tags['area'])
				if areaValue.lower() in ["yes", "1"]:
					isArea = True
				if areaValue.lower() in ["no", "0"]:
					isArea = False

			wayNodes = GetNodesFromWay(w[2], osmParseObj)

			wayInRoi = WayNodesInRoi(wayNodes, bounds)
			
			#print objId, tags, w[2], wayNodes

			if wayInRoi or bounds is None:
				if isArea:
					wayLines.append(('poly', objId, tags, wayNodes[:-1]))
				else:
					wayLines.append(('line', objId, tags, wayNodes))

		#Convert multipolygons in relations
		for objId in osmParseObj.relations:
			w = osmParseObj.relations[objId]
			tags = w[1]
			innerWays = []
			outerWays = []

			if 'type' in tags:
				if  tags['type'] != "multipolygon":
					continue
			else:
				continue
			
			for mem, memData in w[2]:
				role = None
				multiPolyInRoi = False
				if "role" in memData:
					role = memData['role']
				wayLi = GetNodesFromWay(w[2], osmParseObj)
				if role == "inner":
					innerWays.append(wayLi)
				if role == "outer":
					outerWays.append(wayLi)

				checkWayInRoi = WayNodesInRoi(wayNodes, bounds)
				if checkWayInRoi:
					multiPolyInRoi = True

			if multiPolyInRoi:
				wayLines.append(('multipoly', objId, tags, (outerWays, innerWays)))

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
		if finaSplit[1] == ".bz2":
			fi = bz2.BZ2File(fina)
		if finaSplit[1] == ".osm":
			fi = open(fina, "rt")
		if fi is None:
			raise Exception ("Unknown file extension "+str(finaSplit[1]))
		
		self.osmParse = OsmParse()
		self.osmParse.ParseFile(fi)

		print "Read {0} nodes, {1} ways, {2} relations".format(len(self.osmParse.nodes),
			len(self.osmParse.ways),
			len(self.osmParse.relations))

	def GetHighwayNetwork(self, bounds=None, hints={}):

		osmObjToLinesAndPolys = OsmObjToLinesAndPolys()
		osmObjToLinesAndPolys.AddTagOfInterest('highway',"*")
		shapes = osmObjToLinesAndPolys.Do(self.osmParse, bounds)
		return shapes

	def GetRailNetwork(self, bounds=None, hints={}):
		pass

	def GetWater(self, bounds=None, hints={}):
		osmObjToLinesAndPolys = OsmObjToLinesAndPolys()
		osmObjToLinesAndPolys.AddTagOfInterest('waterway',"*")
		osmObjToLinesAndPolys.AddTagOfInterest('water',"*")
		osmObjToLinesAndPolys.AddTagOfInterest('natural',"coastline")
		shapes = osmObjToLinesAndPolys.Do(self.osmParse, bounds)
		return shapes

	def GetLandscape(self, bounds=None, hints={}):
		pass

	def GetContours(self, bounds=None, hints={}):
		pass

	def GetInfrastructure(self, bounds=None, hints={}):
		pass


if __name__ == "__main__":
	
	f = OsmFile("IsleOfWight-Fosm-Oct2013.osm.bz2")
	print len(f.GetHighwayNetwork())

