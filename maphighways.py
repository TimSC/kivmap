from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line, Rectangle

class MapHighways(object):
	def __init__(self):
		self.source = None

	def StartDrawing(self, bounds, zoom, hints):
		#bounds left,bottom,right,top
		return [5]

	def DrawProcessing(self, bounds, zoom, hints, layer, DrawCallback, Proj):
		#bounds left,bottom,right,top
		if self.source is None: return
		if layer != 5: return
		tileLonWidth = bounds[2] - bounds[0]
		tileLonHeight = bounds[3] - bounds[1]

		print "draw layer", layer
		print "bounds", bounds

		highwayNetwork = self.source.GetHighwayNetwork(bounds, hints)
		print "len highwayNetwork", len(highwayNetwork)	

		col = Color(0.3, 0.3, 0.3)
		DrawCallback(col)

		for obj in highwayNetwork:
			if obj[0] != "line": continue
			
			objId = obj[1]
			tags = obj[2]
			wayNodes = obj[3]
			xyPairs = []
			
			for node in wayNodes:
				nodePos = node[1]
				if nodePos is None: continue #Missing node
				x, y = Proj(*nodePos)
				#print nodePos, x, y
				xyPairs.append(x)
				xyPairs.append(y)

			li = Line(points=xyPairs, width=4)
			DrawCallback(li)

	def SetSource(self, source):
		self.source = source


