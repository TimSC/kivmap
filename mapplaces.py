from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.graphics.context_instructions import Scale, PushMatrix, PopMatrix
import graphics

class MapPlaces(object):
	def __init__(self):
		self.source = None
		self.filter = None

		self.highwayDrawOrder = ['motorway',]

		self.styles = {'motorway': {'col': 0x60afd0, 'width': 4}, 
			'trunk' : {'col': 0x6bd470, 'width': 4}, 
			}

	def StartDrawing(self, tileCode, zoom, hints):
		#bounds left,bottom,right,top
		return [15]

	def DrawProcessing(self, tileCode, zoom, hints, layer, DrawCallback, projObjs):
		#bounds left,bottom,right,top
		if self.source is None: return []
		if layer != 15: return []

		#print "draw layer", layer
		#print "bounds", bounds

		places, projInfo = self.filter.Do(tileCode, zoom, hints)
		print "len places", len(places)	
		#for place in places:
		#	print place

		return []

		#Linear scaling to fix tile widget
		if projInfo[0] == "tile":
			DrawCallback(PushMatrix())
			tileSize = projObjs['tile_size']
			DrawCallback(Scale(tileSize[0]/projInfo[1], tileSize[1]/projInfo[2], 1.))

		highwayTypeDict = {}
		for obj in highwayNetwork:
			if obj[0] != "line": continue
			
			objId = obj[1]
			tags = obj[2]
			wayNodes = obj[3]
			xyPairs = []
			if tags['highway'] not in highwayTypeDict:
				highwayTypeDict[tags['highway']] = []
			highwayTypeDict[tags['highway']].append(obj)
			
		#print highwayTypeDict.keys()

		for highwayType in self.highwayDrawOrder[::-1]:
			if highwayType not in highwayTypeDict:
				continue

			for obj in highwayTypeDict[highwayType]:
				shapeType = obj[0]
				objId = obj[1]
				tags = obj[2]
				wayNodes = obj[3]
				dash_length = 1.
				dash_offset = 0.

				highwayType = tags['highway']
				highwayStyle = {}
				if highwayType in self.styles:
					highwayStyle = self.styles[highwayType]
			
				r = 0.3
				g = 0.3
				b = 0.3
				width = 2
				if 'col' in highwayStyle:
					highwayCol = highwayStyle['col']
					r = ((highwayCol >> 16) & 0xff) / 255.
					g = ((highwayCol >> 8) & 0xff) / 255.
					b = (highwayCol & 0xff) / 255.
				if 'width' in highwayStyle:
					width = highwayStyle['width']

				if 'dash_length' in highwayStyle:
					dash_length = highwayStyle['dash_length']
				if 'dash_offset' in highwayStyle:
					dash_offset = highwayStyle['dash_offset']
			
				col = Color(r, g, b)
				DrawCallback(col)

				if shapeType == "line":
					graphics.DrawLine(wayNodes, width, DrawCallback, projObjs, tileCode, zoom, projInfo, dash_length, dash_offset)
				if shapeType == "tripoly":
					graphics.DrawTriPoly(wayNodes, width, DrawCallback, projObjs, tileCode, zoom, projInfo)

		if projInfo[0] == "tile":
			DrawCallback(PopMatrix())

		return []

	def SetSource(self, source):
		self.source = source

		self.filter = self.source.GetQuery("places")
		if self.filter is None:
			self.filter = self.source.CreateQuery("places")
		self.filter.AddTagOfInterest('place',"*")
		

