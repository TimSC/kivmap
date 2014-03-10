
import osmfile, pickle, os

class OsmFileQueryCached(osmfile.OsmFileQuery):
	def __init__(self, parent, name):
		osmfile.OsmFileQuery.__init__(self, parent, name)
		self.storeResultsInCache = True

	def AddTagOfInterest(self, key, val, area = None):
		osmfile.OsmFileQuery.AddTagOfInterest(self, key, val, area = None)

	def Do(self, tileCode, tileZoom, hints):

		cacheFilename = "cache/{0}-{1}-{2}-{3}.dat".format(self.name, tileZoom, tileCode[0], tileCode[1])

		if os.path.exists(cacheFilename):
			return pickle.load(open(cacheFilename, "rb"))

		queryResult = osmfile.OsmFileQuery.Do(self, tileCode, tileZoom, hints)

		if self.storeResultsInCache:
			if not os.path.exists("cache"):
				os.mkdir("cache")
			pickle.dump(queryResult, open(cacheFilename, "wb"))
		return queryResult

class OsmFileCached(osmfile.OsmFile):
	def __init__(self, fina):
		osmfile.OsmFile.__init__(self, fina)

	def CreateQuery(self, name):
		q = OsmFileQueryCached(self, name)
		self.queries[name] = q
		return q

	def GetQuery(self, name):
		if name not in self.queries:
			return None
		return self.queries[name]


if __name__ == "__main__":
	
	f = OsmFileCached("IsleOfWight-Fosm-Oct2013.osm.bz2")
	print len(f.GetHighwayNetwork())

