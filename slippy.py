import math

def deg2num(lat_deg, lon_deg, zoom):
	#http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
	lat_rad = math.radians(lat_deg)
	n = 2.0 ** zoom
	xtile = (lon_deg + 180.0) / 360.0 * n
	ytile = (1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n
	return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
	#http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
	n = 2.0 ** zoom
	lon_deg = xtile / n * 360.0 - 180.0
	lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
	lat_deg = math.degrees(lat_rad)
	return (lat_deg, lon_deg)
