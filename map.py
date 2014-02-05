
#See blog post for ideas: http://blog.jochentopf.com/2011-03-22-new-approaches-for-map-rendering.html

import maphighways

class Map(object):
	def __init__(self):
		self.style = None
		self.source = None
		self.plugins = []
		self.plugins.append(maphighways.MapHighways())

	def SetStyle(self, style):
		self.style = style
	
	def SetSource(self, source):
		self.source = source
		for pl in self.plugins:
			pl.SetSource(source)

	def Draw(self, bounds, zoom, hints):		

		layers = set()

		for pl in self.plugins:
			layers.update(pl.LayersUsed(bounds, zoom, hints))

		layers = list(layers)
		layers.sort()

		for layerNum in layers:
			pl.DrawLayer(bounds, zoom, hints, layerNum)

		#Land and water

		#Land use

		#Transport network

		#Places, administrative and boundaries

		#Labels and icons


	def Route(self, start, end, hints):
		pass


	def GetPoiTree(self):
		pass


	def FindNearbyPois(self, nearLocation, radius, hints):
		pass



	def SearchName(self, searchText, hints):
		pass


