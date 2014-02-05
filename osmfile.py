
import bz2, os
import xml.parsers.expat as expat
from xml.sax.saxutils import escape, quoteattr

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
		wayLines = []
		for objId in self.osmParse.ways:
			w = self.osmParse.ways[objId]
			tags = w[1]
			if 'highway' not in tags:
				continue

			wayNodes = []
			for ntag, nid in w[2]:
				nidInt = int(nid['ref'])
				if nidInt not in self.osmParse.nodes:
					wayNodes.append((nidInt, None, None, None))
					continue
				nodeObj = self.osmParse.nodes[nidInt]	
				nodeAttrs = nodeObj[0]
				nodeTags = nodeObj[1]
				wayNodes.append((nidInt, (float(nodeAttrs['lat']), float(nodeAttrs['lon'])), nodeAttrs, nodeTags))

			#print objId, tags, w[2], wayNodes

			wayLines.append(('line', objId, tags, wayNodes))
		return wayLines

	def GetRailNetwork(self):
		pass

	def GetWater(self):
		pass

	def GetLandscape(self):
		pass

	def GetContours(self):
		pass

	def GetInfrastructure(self):
		pass


if __name__ == "__main__":
	
	f = OsmFile("IsleOfWight-Fosm-Oct2013.osm.bz2")
	print len(f.GetHighwayNetwork())

