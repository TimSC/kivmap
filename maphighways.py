
class MapHighways(object):
	def __init__(self):
		self.source = None

	def StartDrawing(self, bounds, zoom, hints):
		return [5]

	def DrawProcessing(self, bounds, zoom, hints, layer):
		print "draw layer", layer
		if self.source is None: return

		highwayNetwork = self.source.GetHighwayNetwork()
		print len(highwayNetwork)

	def SetSource(self, source):
		self.source = source


