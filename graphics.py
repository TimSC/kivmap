from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line, Rectangle, Mesh, Triangle
from pyshull.earclipping import EarClipping
import pickle, random

gKeepProblemPolygons = False

def DrawLine(obj, width, DrawCallback, Proj, dash_length = 1., dash_offset = 0.):

	xyPairs = []
	for node in obj:
		nodePos = node[1]
		if nodePos is None: continue #Missing node
		x, y = Proj(*nodePos)
		#print nodePos, x, y
		xyPairs.append(x)
		xyPairs.append(y)

	li = Line(points=xyPairs, width=width)

	if dash_length != 1. or dash_offset != 0.:
		li.width = 1.0 #Kivy only supports dashes with width of 1
		li.dash_length = 10.
		li.dash_offset = 10.
	DrawCallback(li)

def DrawPoly(obj, width, DrawCallback, Proj):

	vertices = []
	for node in obj:
		nodePos = node[1]
		if nodePos is None: continue #Missing node
		x, y = Proj(*nodePos)
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

def DrawTriPoly(obj, width, DrawCallback, Proj):

	vertices2 = []
	for node in obj[0]:
		if node is None: continue #Missing node
		x, y = Proj(*node)
		vertices2.append((x, y))

	triangles = obj[1]

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


def DrawPolyWithHoles(singleOuterPoly, width, DrawCallback, Proj):

	vertices = []
	innerVertices = []
	outerWay = singleOuterPoly[0]
	innerWays = singleOuterPoly[1]
	for node in outerWay:
		nodePos = node[1]
		if nodePos is None: continue #Missing node
		x, y = Proj(*nodePos)
		vertices.append((x, y))

	for innerWay in innerWays:
		innerWayVertices = []
		for node in innerWay:
			nodePos = node[1]
			if nodePos is None: continue #Missing node
			x, y = Proj(*nodePos)
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

def DrawMultiPoly(obj, width, DrawCallback, Proj):	
	for singleOuterPoly in obj:
		DrawPolyWithHoles(singleOuterPoly, width, DrawCallback, Proj)

