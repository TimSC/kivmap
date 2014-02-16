from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line, Rectangle, Mesh, Triangle
from pyshull.earclipping import EarClipping
import pickle, random

gKeepProblemPolygons = False

def DrawLine(obj, width, DrawCallback, Proj):

	xyPairs = []
	for node in obj:
		nodePos = node[1]
		if nodePos is None: continue #Missing node
		x, y = Proj(*nodePos)
		#print nodePos, x, y
		xyPairs.append(x)
		xyPairs.append(y)

	li = Line(points=xyPairs, width=width)
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

def DrawMultiPoly(obj, width, DrawCallback, Proj):

	vertices = []
	innerVertices = []
	outerWay = obj[0]
	innerWays = obj[1]
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

	try:
		vertices2, triangles = EarClipping(vertices, innerVertices)
	except Exception as err:
		print err
		if gKeepProblemPolygons:
			randFilename = "polyerr{0}.dat".format(random.randint(0,1000000))
			pickle.dump((vertices, innerVertices), open(randFilename, "wb"))
			print "Saved err polygon to", randFilename
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

