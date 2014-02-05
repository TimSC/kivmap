
#See blog post for ideas: http://blog.jochentopf.com/2011-03-22-new-approaches-for-map-rendering.html

class Map(object):
	def __init__(self):
		self.source = None
		self.plugins = []
		
	def AddPlugin(self, plugin):
		self.plugins.append(plugin)

	def Draw(self, bounds, zoom, hints, DrawCallback, Proj):		

		processingSteps = set()

		for pl in self.plugins:
			steps = pl.StartDrawing(bounds, zoom, hints)
			for step in steps:
				processingSteps.add((step, pl))

		while len(processingSteps) > 0:
			sortableSteps = list(processingSteps)
			sortableSteps.sort()
			nextStep = sortableSteps[0]
			processingSteps.discard(nextStep)

			nextStep[1].DrawProcessing(bounds, zoom, hints, nextStep[0], DrawCallback, Proj)

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


