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
	projCode = obj[1][0]

	if projCode == "wgs84":
		for node in obj[0]:
			if nodePos is None: continue #Missing node

			x, y = Proj(nodePos[0], nodePos[1], projObjs)
			#print nodePos, x, y
			xyPairs.append(x)
			xyPairs.append(y)

	if projCode == "tile":
		tileSize = projObjs['tile_size']
		dataResolutionWidth = obj[1][1]
		dataResolutionHeight = obj[1][2]

		xyPairs = []
		pts = obj[0]
		for i in range(0, len(pts), 2):
			xyPairs.extend((pts[i] * tileSize[0] / dataResolutionWidth, pts[i+1] * tileSize[1] / dataResolutionHeight))


		#xyPairs = obj[0]

	li = Line(points=xyPairs, width=width)

	if dash_length != 1. or dash_offset != 0.:
		li.width = 1.0 #Kivy only supports dashes with width of 1
		li.dash_length = 10.
		li.dash_offset = 10.
	DrawCallback(li)

def DrawTriPoly(obj, width, DrawCallback, projObjs, tileCode, tileZoom):

	vertices2 = []
	projCode = obj[2][0]

	if projCode == "wgs84":
		for nodePos in obj[0]:
			if nodePos is None: continue #Missing node
			#print nodePos
			x, y = Proj(nodePos[0], nodePos[1], projObjs)
			vertices2.extend((x, y))

	if projCode == "tile":
		tileSize = projObjs['tile_size']
		dataResolutionWidth = obj[2][1]
		dataResolutionHeight = obj[2][2]

		pts = obj[0]
		for i in range(0, len(pts), 2):
			vertices2.extend((pts[i] * tileSize[0] / dataResolutionWidth, pts[i+1] * tileSize[1] / dataResolutionHeight))

	triangles = obj[1]
	dataProj = obj[2]
	#print dataProj

	#print triangles
	for tri in triangles:
		for ptNum in tri:
			if 2*ptNum < 0 or 2*ptNum+1 >= len(vertices2):
				raise Exception("Out of bounds vertex index "+str(ptNum)+","+str(len(vertices2)))

	for tri in triangles:
		triPos = []
		for p in tri:
			triPos.extend((vertices2[2*p], vertices2[2*p+1]))

		poly = Triangle(points = triPos)
		DrawCallback(poly)

