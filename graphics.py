from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line, Rectangle, Mesh, Triangle
import pickle, random, slippy, math

gKeepProblemPolygons = False

def Proj(lat_deg, lon_deg, projObjs):
	ProjFunc = projObjs['wgs84']
	return ProjFunc(lat_deg, lon_deg)

def DrawLine(obj, width, DrawCallback, projObjs, tileCode, tileZoom, projInfo, dash_length = 1., dash_offset = 0.):

	xyPairs = []
	projCode = projInfo[0]

	if projCode == "wgs84":
		for node in obj[0]:
			if nodePos is None: continue #Missing node

			x, y = Proj(nodePos[0], nodePos[1], projObjs)
			#print nodePos, x, y
			xyPairs.append(x)
			xyPairs.append(y)

	if projCode == "tile":
		tileSize = projObjs['tile_size']
		dataResolutionWidth = projInfo[1]
		dataResolutionHeight = projInfo[2]
		xyPairs = obj[0]

	li = Line(points=xyPairs, width=width)

	if dash_length != 1. or dash_offset != 0.:
		li.width = 1.0 #Kivy only supports dashes with width of 1
		li.dash_length = 10.
		li.dash_offset = 10.
	DrawCallback(li)

def TriPointPos(pts, tri):
	triPos = []
	for p in tri:
		triPos.extend((pts[2*p], pts[2*p+1]))
	return triPos

def DrawTris(vertices2, triangles, DrawCallback):
	for tri in triangles:
		triPos = TriPointPos(vertices2, tri)

		poly = Triangle(points = triPos)
		DrawCallback(poly)

def DrawTriPoly(obj, width, DrawCallback, projObjs, tileCode, tileZoom, projInfo):

	vertices2 = []
	projCode = projInfo[0]

	if projCode == "wgs84":
		for nodePos in obj[0]:
			if nodePos is None: continue #Missing node
			#print nodePos
			x, y = Proj(nodePos[0], nodePos[1], projObjs)
			vertices2.extend((x, y))

	if projCode == "tile":
		tileSize = projObjs['tile_size']
		dataResolutionWidth = projInfo[1]
		dataResolutionHeight = projInfo[2]
		vertices2 = obj[0]

	triangles = obj[1]

	#print triangles
	indexCheck = False
	if indexCheck:
		for tri in triangles:
			for ptNum in tri:
				if 2*ptNum < 0 or 2*ptNum+1 >= len(vertices2):
					raise Exception("Out of bounds vertex index "+str(ptNum)+","+str(len(vertices2)))

	DrawTris(vertices2, triangles, DrawCallback)

