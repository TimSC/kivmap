from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line, Rectangle, Mesh, Triangle
import pickle, random, slippy, math

gKeepProblemPolygons = False

def Proj(lat_deg, lon_deg, projObjs):
	ProjFunc = projObjs['wgs84']
	return ProjFunc(lat_deg, lon_deg)

def DrawLine(obj, width, DrawCallback, projObjs, tileCode, tileZoom, dash_length = 1., dash_offset = 0.):

	xyPairs = []
	for node in obj[0]:
		nodePos = node[1]
		if nodePos is None: continue #Missing node

		x, y = Proj(nodePos[0], nodePos[1], projObjs)
		#print nodePos, x, y
		xyPairs.append(x)
		xyPairs.append(y)

	li = Line(points=xyPairs, width=width)

	if dash_length != 1. or dash_offset != 0.:
		li.width = 1.0 #Kivy only supports dashes with width of 1
		li.dash_length = 10.
		li.dash_offset = 10.
	DrawCallback(li)

def DrawTriPoly(obj, width, DrawCallback, projObjs, tileCode, tileZoom):

	vertices2 = []
	for nodePos in obj[0]:
		if nodePos is None: continue #Missing node
		#print nodePos
		x, y = Proj(nodePos[0], nodePos[1], projObjs)
		vertices2.append((x, y))

	triangles = obj[1]
	dataProj = obj[2]
	#print dataProj

	#print triangles
	for tri in triangles:
		for ptNum in tri:
			if ptNum < 0 or ptNum >= len(vertices2):
				raise Exception("Out of bounds vertex index")

	for tri in triangles:
		triPos = []
		for p in tri:
			triPos.extend(list(vertices2[p]))

		poly = Triangle(points = triPos)
		DrawCallback(poly)

