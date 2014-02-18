from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line, Rectangle, Mesh, Triangle
from pyshull.earclipping import EarClipping
import pickle, random, slippy, math

gKeepProblemPolygons = False

def Proj(lat_deg, lon_deg, xtile, ytile, zoom, tileWidth, tileHeight):
	lat_rad = math.radians(lat_deg)
	n = 2.0 ** zoom

	normXtile = ((lon_deg + 180.0) / 360.0 * n) - xtile
	normYtile = ((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n) - ytile
	if 1:
		normYtile = 1. - normYtile #Flip vertically

	return (normXtile * tileWidth, normYtile * tileHeight)

def DrawLine(obj, width, DrawCallback, tileSize, projCode, tileCode, tileZoom, dash_length = 1., dash_offset = 0.):

	xyPairs = []
	for node in obj:
		nodePos = node[1]
		if nodePos is None: continue #Missing node

		x, y = Proj(nodePos[0], nodePos[1], tileCode[0], tileCode[1], tileZoom, *tileSize)
		#print nodePos, x, y
		xyPairs.append(x)
		xyPairs.append(y)

	li = Line(points=xyPairs, width=width)

	if dash_length != 1. or dash_offset != 0.:
		li.width = 1.0 #Kivy only supports dashes with width of 1
		li.dash_length = 10.
		li.dash_offset = 10.
	DrawCallback(li)

def DrawPoly(obj, width, DrawCallback, tileSize, projCode, tileCode, tileZoom):

	vertices = []
	for node in obj:
		nodePos = node[1]
		if nodePos is None: continue #Missing node
		x, y = Proj(nodePos[0], nodePos[1], tileCode[0], tileCode[1], tileZoom, *tileSize)
		vertices.append((x, y))

	try:
		vertices2, triangles = EarClipping(vertices, [])
	except Exception as err:
		print err
		if gKeepProblemPolygons:
			randFilename = "polyerr{0}.dat".format(random.randint(0,1000000))
			pickle.dump((vertices, []), open(randFilename, "wb"))
			print "Saved err polygon to", randFilename
		return

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

def DrawTriPoly(obj, width, DrawCallback, tileSize, projCode, tileCode, tileZoom):

	vertices2 = []
	for nodePos in obj[0]:
		if nodePos is None: continue #Missing node
		x, y = Proj(nodePos[0], nodePos[1], tileCode[0], tileCode[1], tileZoom, *tileSize)
		vertices2.append((x, y))

	triangles = obj[1]
	dataProj = obj[2]
	print dataProj

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


def DrawPolyWithHoles(singleOuterPoly, width, DrawCallback, tileSize, projCode, tileCode, tileZoom):

	vertices = []
	innerVertices = []
	outerWay = singleOuterPoly[0]
	innerWays = singleOuterPoly[1]
	for node in outerWay:
		nodePos = node[1]
		if nodePos is None: continue #Missing node
		x, y = Proj(nodePos[0], nodePos[1], tileCode[0], tileCode[1], tileZoom, *tileSize)
		vertices.append((x, y))

	for innerWay in innerWays:
		innerWayVertices = []
		for node in innerWay:
			nodePos = node[1]
			if nodePos is None: continue #Missing node
			x, y = Proj(nodePos[0], nodePos[1], tileCode[0], tileCode[1], tileZoom, *tileSize)
			innerWayVertices.append((x, y))
		innerVertices.append(innerWayVertices)

	if len(vertices) == 0:
		return

	#Triangularise shape
	try:
		vertices2, triangles = EarClipping(vertices, innerVertices)
	except Exception as err:
		#Problems encountered
		print err
		if gKeepProblemPolygons:
			randFilename = "polyerr{0}.dat".format(random.randint(0,1000000))
			pickle.dump((vertices, innerVertices), open(randFilename, "wb"))
			print "Saved err polygon to", randFilename
		try:
			#Try to triangularise by ignoring holes
			vertices2, triangles = EarClipping(vertices, [])
		except Exception as err:
			return

	#if len(innerVertices) == 0: return
	
	for tri in triangles:
		for ptNum in tri:
			if ptNum < 0 or ptNum >= len(vertices2):
				raise Exception("Out of bounds vertex index")

	#print triangles

	for tri in triangles:
		triPos = []
		for p in tri:
			triPos.extend(list(vertices2[p]))
		#print triPos

		poly = Triangle(points = triPos)
		DrawCallback(poly)

def DrawMultiPoly(obj, width, DrawCallback, tileSize, projCode, tileCode, tileZoom):
	for singleOuterPoly in obj:
		DrawPolyWithHoles(singleOuterPoly, width, DrawCallback, tileSize, projCode, tileCode, tileZoom)


