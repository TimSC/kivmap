
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
import kivy.metrics as metrics
from kivy.clock import Clock
import tile, slippy, osmfilecached, map, maphighways, mapwater, maplandscape, mapplaces

class MapLayer(RelativeLayout):
	def __init__(self, **args):
		RelativeLayout.__init__(self, **args)
		self.lastTouch = None
		self.tiles = {}
		self.viewPos = (50.7, -1.3)
		self.viewZoom = 14
		self.unscaledTileSize = 512
		self.tileSize = metrics.dp(self.unscaledTileSize)
		self.map = map.Map()

		#source = osmfile.OsmFile("Simple.osm.gz")
		source = osmfilecached.OsmFileCached("IsleOfWight-Fosm-Oct2013.osm.gz")

		highways = maphighways.MapHighways()
		highways.SetSource(source)
		self.map.AddPlugin(highways)

		water = mapwater.MapWater()
		water.SetSource(source)
		self.map.AddPlugin(water)

		places = mapplaces.MapPlaces()
		places.SetSource(source)
		self.map.AddPlugin(places)

		landscape = maplandscape.MapLandscape()
		landscape.SetSource(source)
		self.map.AddPlugin(landscape)

		Clock.schedule_interval(self.LateRendering, 0.1)

		self.bind(pos=self.update_graphics_pos,
			size=self.update_graphics_size)

	def on_touch_down(self, touch):
		print "layer touch"
		self.lastTouch = touch.pos

	def on_touch_move(self, touch):
		#Calculate distance dragged
		relativeMove = (touch.pos[0] - self.lastTouch[0], touch.pos[1] - self.lastTouch[1])
		self.lastTouch = touch.pos
		fractRelativeMove = (relativeMove[0] / self.size[0], relativeMove[1] / self.size[1])

		#Update view
		left, right, top, bottom = self.GetViewBounds() 
		dx = (right - left) * fractRelativeMove[0]
		dy = (bottom - top) * fractRelativeMove[1]
		tilex, tiley = slippy.deg2num(self.viewPos[0], self.viewPos[1], self.viewZoom)
		tilex -= dx
		tiley += dy
		self.viewPos = slippy.num2deg(tilex, tiley, self.viewZoom)

		self.UpdateExistingTilePositions()
		self.AddNewTilesAsRequired()
		self.RemoveUnneededTiles()

	def UpdateExistingTilePositions(self):

		#Update existing widget positions
		left, right, top, bottom = self.GetViewBounds() 
		for x in self.tiles:
			tileRow = self.tiles[x]
			for y in tileRow:
				winPos = (x - left) * self.size[0] / (right - left), (bottom - (y+1)) * self.size[1] / (bottom - top)
				ti = tileRow[y]
				ti.pos = winPos

	def GetViewBounds(self):
		tilex, tiley = slippy.deg2num(self.viewPos[0], self.viewPos[1], self.viewZoom)
		#print tilex, tiley

		left = tilex - 0.5 * self.size[0] / self.tileSize
		right = tilex + 0.5 * self.size[0] / self.tileSize
		top = tiley - 0.5 * self.size[1] / self.tileSize
		bottom = tiley + 0.5 * self.size[1] / self.tileSize

		return left, right, top, bottom

	def AddNewTilesAsRequired(self):
		left, right, top, bottom = self.GetViewBounds()
		#print left, right, top, bottom
		rleft = int(left)
		rright = int(right) + 1
		rtop = int(top)
		rbottom = int(bottom) + 1
		#print rleft, rright, rtop, rbottom 
		
		
		for x in range(rleft, rright):
			if x not in self.tiles:
				self.tiles[x] = {}
			tileRow = self.tiles[x]
			for y in range(rtop, rbottom):
				if y not in tileRow:
					print "Add widget", x, y
					winPos = (x - left) * self.size[0] / (right - left), (bottom - (y+1)) * self.size[1] / (bottom - top)
					#print x, y, "winPos", winPos
					ti = tile.TileWidget(size=(self.tileSize,self.tileSize), pos=winPos)
					ti.SetTileNum(x, y, self.viewZoom)
					ti.SetMap(self.map)
					#ti.Draw()
					tileRow[y] = ti
					self.add_widget(tileRow[y])

	def RemoveUnneededTiles(self):
		left, right, top, bottom = self.GetViewBounds()
		#print left, right, top, bottom
		rleft = int(left)
		rright = int(right) + 1
		rtop = int(top)
		rbottom = int(bottom) + 1
		#print rleft, rright, rtop, rbottom 
		
		for x in self.tiles:
			tileRow = self.tiles[x]
			tilesToRemove = []
			for y in tileRow:
				if y < rtop or y >= rbottom:
					tilesToRemove.append(y)

			for y in tilesToRemove:
				print "Remove widget", x, y
				self.remove_widget(tileRow[y])
				del tileRow[y]

	def update_graphics_size(self, instance, value):
		print "layout update_graphics_size", self.size_hint, self.size
		self.UpdateExistingTilePositions()
		self.AddNewTilesAsRequired()
		self.RemoveUnneededTiles()

	def update_graphics_pos(self, instance, value):
		pass

	def LateRendering(self, arg):
		for x in self.tiles:
			tileRow = self.tiles[x]
			for y in tileRow:
				ti = tileRow[y]
				if ti.IsDrawDone(): continue
				ti.Draw()
				return True

		return True

