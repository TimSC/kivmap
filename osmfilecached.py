
import osmfile

class OsmFileQueryCached(osmfile.OsmFileQuery):
	def __init__(self, parent, name):
		osmfile.OsmFileQuery.__init__(parent, name)

	def AddTagOfInterest(self, key, val, area = None):
		osmfile.OsmFileQuery.AddTagOfInterest(key, val, area = None)

	def Do(self, tileCode, tileZoom, hints):
		return osmfile.OsmFileQuery.Do(tileCode, tileZoom, hints)

class OsmFileCached(osmfile.OsmFile):
	def __init__(self, fina):
		osmfile.OsmFile.__init__(self, fina)

	def CreateQuery(self, name):
		return osmfile.OsmFile.CreateQuery(self, name)

	def GetQuery(self, name):
		return osmfile.OsmFile.GetQuery(self, name)

if __name__ == "__main__":
	
	f = OsmFileCached("IsleOfWight-Fosm-Oct2013.osm.bz2")
	print len(f.GetHighwayNetwork())

