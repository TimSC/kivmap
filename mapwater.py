from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line, Rectangle, Mesh, Triangle
from kivy.graphics.context_instructions import Scale, PushMatrix, PopMatrix
import graphics

class MapWater(object):
	def __init__(self):
		self.source = None
		self.filter = None

		self.drawOrder = ['coastline', 'water', 'river', 'stream', 'canal']

		self.styles = {'coastline': {'col': 0x0000d0, 'width': 2},
			'water': {'col': 0x000000},
			}

	def StartDrawing(self, tileCode, zoom, hints):
		#bounds left,bottom,right,top
		return [0]

	def DrawProcessing(self, tileCode, zoom, hints, layer, DrawCallback, projObjs):
		#bounds left,bottom,right,top
		if self.source is None: return
		if layer != 0: return

		#print "draw layer", layer
		#print "bounds", bounds

		water, projInfo = self.filter.Do(tileCode, zoom, hints)
		#print "len water", len(water)	

		#Linear scaling to fix tile widget
		if projInfo[0] == "tile":
			DrawCallback(PushMatrix())
			tileSize = projObjs['tile_size']
			DrawCallback(Scale(tileSize[0]/projInfo[1], tileSize[1]/projInfo[2], 1.))

		typeDict = {}
		for obj in water:
			
			objId = obj[1]
			tags = obj[2]
			wayNodes = obj[3]
			xyPairs = []

			primaryKey = None
			primaryType = None
			if 'natural' in tags:
				primaryKey = 'natural'
				primaryType = tags['natural']
			if 'waterway' in tags:
				primaryKey = 'waterway'
				primaryType = tags['waterway']
			if primaryType is None:
				continue

			if primaryType not in typeDict:
				typeDict[primaryType] = []

			typeDict[primaryType].append((primaryKey, primaryType, obj))
			
		#print typeDict.keys()

		for drawType in self.drawOrder[::-1]:
			if drawType not in typeDict:
				continue

			for primaryKey, primaryType, obj in typeDict[drawType]:
				shapeType = obj[0]
				objId = obj[1]
				tags = obj[2]
				wayNodes = obj[3]

				renderStyle = {}
				if primaryType in self.styles:
					renderStyle = self.styles[primaryType]
			
				r = 0.0
				g = 0.0
				b = 0.7
				width = 2
				if 'col' in renderStyle:
					col = renderStyle['col']
					r = ((col >> 16) & 0xff) / 255.
					g = ((col >> 8) & 0xff) / 255.
					b = (col & 0xff) / 255.
				if 'width' in renderStyle:
					width = renderStyle['width']
			
				col = Color(r, g, b)
				DrawCallback(col)

				if shapeType == "line":
					graphics.DrawLine(wayNodes, width, DrawCallback, projObjs, tileCode, zoom, projInfo)
				if shapeType == "tripoly":
					graphics.DrawTriPoly(wayNodes, width, DrawCallback, projObjs, tileCode, zoom, projInfo)

		if projInfo[0] == "tile":
			DrawCallback(PopMatrix())

		return []

	def SetSource(self, source):
		self.source = source

		self.filter = self.source.GetQuery("landscape")
		if self.filter is None:
			self.filter = self.source.CreateQuery("landscape")

		self.filter.AddTagOfInterest('waterway',"*")
		self.filter.AddTagOfInterest('water',"*")
		self.filter.AddTagOfInterest('natural',"coastline", 0)

