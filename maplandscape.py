from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line, Rectangle, Mesh, Triangle
import graphics

class MapLandscape(object):
	def __init__(self):
		self.source = None

		self.drawOrder = ['residential', 'retail', 'residential', 'recreation_ground', 'industrial',
			'greenfield', 'cemetery', 'brownfield', 'allotments', 'landfill', 'forest', 'construction'
			, 'wood']

		self.styles = {'residential': {'fillcol': 0xefefef}, 
			'retail': {'fillcol': 0xfff1f1}, 
			'commercial': {'fillcol': 0xfffdec}, 
			'recreation_ground': {'fillcol': 0xf1ffd7},
			'greenfield': {'fillcol': 0xfffee5}, 
			'brownfield': {'fillcol': 0xfffee5}, 
			'cemetery': {'fillcol': 0xf1ffd7}, 
			'allotments': {'fillcol': 0xf1ffd7}, 
			'landfill': {'fillcol': 0xfffee5}, 
			'industrial': {'fillcol': 0xfffee5}, 
			'forest': {'fillcol': 0x5ed74a},
			'wood': {'fillcol': 0x5ed74a},  
			'construction': {'fillcol': 0xfffee5},
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

		objs, projInfo = self.source.GetLandscape(tileCode, zoom, hints)
		#print "len objs", len(objs)

		typeDict = {}
		for obj in objs:
			
			objId = obj[1]
			tags = obj[2]
			wayNodes = obj[3]
			xyPairs = []

			primaryKey = None
			primaryType = None
			if 'landuse' in tags:
				primaryKey = 'landuse'
				primaryType = tags['landuse']
			if 'natural' in tags:
				primaryKey = 'natural'
				primaryType = tags['natural']
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
				#if shapeType == "multipoly":
				#	print wayNodes

				renderStyle = {}
				if primaryType in self.styles:
					renderStyle = self.styles[primaryType]
			
				r = 0.9
				g = 0.9
				b = 0.9
				width = 2
				if 'fillcol' in renderStyle:
					col = renderStyle['fillcol']
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

		return []

	def SetSource(self, source):
		self.source = source


