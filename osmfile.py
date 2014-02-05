
import bz2, os
import xml.parsers.expat as expat
from xml.sax.saxutils import escape, quoteattr

class ExpatParse(object):
	def __init__(self):
		self.parser = expat.ParserCreate()
		self.parser.CharacterDataHandler = self.HandleCharData
		self.parser.StartElementHandler = self.HandleStartElement
		self.parser.EndElementHandler = self.HandleEndElement
		self.depth = 0
		self.tags = []
		self.attr = []

	def ParseFile(self, fi):
		self.fiTmp = fi
		self.parser.ParseFile(fi)

	def HandleCharData(self, data):
		pass

	def HandleStartElement(self, name, attrs):
		self.depth += 1
		self.tags.append(name)
		self.attr.append(attrs)
		print tag, attrs

	def HandleEndElement(self, name): 
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
		
		expatParse = ExpatParse()
		expatParse.ParseFile(fi)

	def GetRoadNetwork(self):
		pass

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

