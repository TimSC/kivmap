
#See blog post for ideas: http://blog.jochentopf.com/2011-03-22-new-approaches-for-map-rendering.html

class Map(object):
	def __init__(self):
		self.source = None
		self.plugins = []
		
	def AddPlugin(self, plugin):
		self.plugins.append(plugin)

	def Draw(self, tileCode, zoom, hints, DrawCallback, projObjs):

		processingSteps = set()

		#Get initial list of steps to perform rendering
		for pl in self.plugins:
			steps = pl.StartDrawing(tileCode, zoom, hints)
			for step in steps:
				processingSteps.add((step, pl))

		while len(processingSteps) > 0:
			sortableSteps = list(processingSteps)
			sortableSteps.sort()
			nextStep = sortableSteps[0]
			processingSteps.discard(nextStep)

			extraSteps = nextStep[1].DrawProcessing(tileCode, zoom, hints, nextStep[0], DrawCallback, projObjs)

			#Append extra steps to task list
			for step in extraSteps:
				processingSteps.add((step, nextStep[1]))

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


