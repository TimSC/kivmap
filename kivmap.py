from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.core.window import Window
import kivy.metrics as metrics
import random, slippy

class TileWidget(Widget):

	def __init__(self, **args):
		Widget.__init__(self, **args)
		self.objs = []

		with self.canvas:
			Color(1., 1., 0)
			self.objs.append(Rectangle(pos=self.pos, size=(self.width, self.height)))
			Color(0, 0.7, 0)
			self.objs.append(Ellipse(pos=self.pos, size=self.size))

		self.bind(pos=self.update_graphics_pos,
			size=self.update_graphics_size)

	def on_touch_down(self, touch):
		pass

	def on_touch_move(self, touch):
		pass

	def update_graphics_pos(self, instance, value):
		for obj in self.objs:
			obj.pos = value

	def update_graphics_size(self, instance, value):
		#print "widget update_graphics_size"
		pass

class MapLayer(RelativeLayout):
	def __init__(self, **args):
		RelativeLayout.__init__(self, **args)
		self.lastTouch = None
		self.tiles = {}
		self.viewPos = (50.7, -1.3)
		self.viewZoom = 12
		self.tileSize = metrics.dp(200)

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
		tiley -= dy
		self.viewPos = slippy.num2deg(tilex, tiley, self.viewZoom)

		self.UpdateExistingTilePositions()
		self.AddNewTilesAsRequired()

	def UpdateExistingTilePositions(self):

		#Update existing widget positions
		left, right, top, bottom = self.GetViewBounds() 
		for x in self.tiles:
			tileRow = self.tiles[x]
			for y in tileRow:
				winPos = (x - left) * self.size[0] / (right - left), (y - top) * self.size[1] / (bottom - top)
				ti = tileRow[y]
				ti.pos = winPos

	def GetViewBounds(self):
		tilex, tiley = slippy.deg2num(self.viewPos[0], self.viewPos[1], self.viewZoom)

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
					winPos = (x - left) * self.size[0] / (right - left), (y - top) * self.size[1] / (bottom - top)
					#print x, y, "winPos", winPos
					tileRow[y] = TileWidget(size=(self.tileSize,self.tileSize), pos=winPos)
					self.add_widget(tileRow[y])

	def update_graphics_size(self, instance, value):
		print "layout update_graphics_size", self.size_hint, self.size
		self.UpdateExistingTilePositions()
		self.AddNewTilesAsRequired()	

	def update_graphics_pos(self, instance, value):
		pass

class KivMapApp(App):

	def __init__(self, **args):

		App.__init__(self, **args)

	def build(self):
		return MapLayer(size_hint=(1., 1.))


if __name__ == '__main__':
	KivMapApp().run()

