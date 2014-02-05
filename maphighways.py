
class MapHighways(object):
	def __init__(self):
		self.source = None

	def StartDrawing(self, bounds, zoom, hints):
		return [5]

	def DrawProcessing(self, bounds, zoom, hints, layer):
		print "draw layer", layer

	def SetSource(self, source):
		self.source = source


