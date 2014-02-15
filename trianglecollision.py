from pyshull import earclipping

def DoTrianglesCollide(tri1, tri2):
	#Do bounding box check

	#Check for line overlaps
	for i in range(3):
		for j in range(3):
			crossing = earclipping.LineSegmentIntersection((tri1[i],tri1[(i+1)%3]),(tri2[i],tri2[(j+1)%3]))
			if crossing: return True

	#Check for entirely contained triangle

	return False


def CheckResult(expected, actual, description):
	if expected == actual:
		print "Test OK"
	else:
		print "Test Failed:", description
	return expected == actual

def ReorderTriangleThenTest(tri1, tri2, swap, expected, description):
	if not swap:
		result = DoTrianglesCollide(tri1, tri2)
		CheckResult(expected, result, description)
	else:
		result = DoTrianglesCollide(tri1, tri2[::-1])
		CheckResult(expected, result, description)

def RunTriangleTestBattery(tri1, tri2, expected, description):
	ReorderTriangleThenTest(tri1, tri2, 0, expected, description)
	ReorderTriangleThenTest(tri1, tri2, 1, expected, description)
	ReorderTriangleThenTest(tri2, tri1, 0, expected, description)
	ReorderTriangleThenTest(tri2, tri1, 1, expected, description)
	

if __name__ == "__main__":
	#Unit tests

	#Identical triangle
	RunTriangleTestBattery(((0.,0.),(1.,0.),(0.5,1.)),((0.,0.),(1.,0.),(0.5,1.)), 
		True, "Identical triangle")

	#Overlapping triangles, crossing edge, point on edge
	RunTriangleTestBattery(((0.5,0.),(1.5,0.),(1.5,1.)),((0.,0.),(1.,0.),(0.5,1.)), 
		True, "Overlapping triangles, crossing edge, point on edge")

	#Overlapping triangles, crossing edge, point is interior
	RunTriangleTestBattery(((0.0,0.5),(1.,0.),(1.,1.)),((0.5,0.5),(1.5,0.),(1.5,1.)),
		True, "Overlapping triangles, crossing edge, point is interior")

	#Non overlapping triangles
	RunTriangleTestBattery(((0.,0.),(1.,0.),(0.5,1.)),((10.,0.),(11.,0.),(10.5,1.)),
		False, "Non overlapping triangles")

	#Nearby, non overlapping triangles
	RunTriangleTestBattery(((0.,0.),(1.,0.),(0.5,1.)),((0.6,1.),(1.1,0.),(1.6,1.)),
		False, "Nearby, non overlapping triangles")

	#Common point, no crossing
	RunTriangleTestBattery(((0.,0.),(1.,0.),(0.5,1.)),((0.,10.0),(1.,10.),(0.5,1.)),
		True, "Common point, no crossing")

	#Shared edge, no crossing
	RunTriangleTestBattery(((0.,0.),(1.,0.),(0.5,1.)),((0.,0.),(1.,0.),(0.5,-1.)),
		True, "Common point, no crossing")

	#Contained triangle
	RunTriangleTestBattery(((0.,0.),(10.,0.),(5.,10.)),((4.,1.),(6.,1.),(5.,1.)),
		True, "Contained triangle")



	#result = DoTrianglesCollide(((),(),()),((),(),()))

	#result = DoTrianglesCollide(((),(),()),((),(),()))
