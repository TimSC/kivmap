from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line, Rectangle, Mesh, Triangle
from pyshull.earclipping import EarClipping

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

	vertices2, triangles = EarClipping(vertices, [])
	
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
	outerWay = obj[0]
	innerWays = obj[1]
	for node in outerWay:
		nodePos = node[1]
		if nodePos is None: continue #Missing node
		x, y = Proj(*nodePos)
		vertices.append((x, y))

	if len(vertices) == 0:
		return

	try:
		vertices2, triangles = EarClipping(vertices, [])
	except Exception as err:
		print err
		return
	
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

