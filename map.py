
#See blog post for ideas: http://blog.jochentopf.com/2011-03-22-new-approaches-for-map-rendering.html

class Map(object):
	def __init__(self):
		self.style = None
		self.source = None

	def SetStyle(self, style):
		self.style = style
	
	def SetSource(self, source):
		self.source = source

	def Draw(self, dimensions, zoom, hints):
		pass		

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


