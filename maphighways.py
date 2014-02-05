
class MapHighways(object):
	def __init__(self):
		self.source = None

	def LayersUsed(self, bounds, zoom, hints):
		return [5]

	def DrawLayer(self, bounds, zoom, hints, layer):
		pass

	def SetSource(self, source):
		self.source = source


