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

	def SetSource(self, source):
		self.source = source

		self.filter = self.source.GetQuery("places")
		if self.filter is None:
			self.filter = self.source.CreateQuery("places", "wgs84")
		self.filter.AddTagOfInterest('place',"*")
		

