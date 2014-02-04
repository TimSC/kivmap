from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.core.window import Window
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
		print "widget update_graphics_size"

class MapLayer(RelativeLayout):
	def __init__(self, **args):
		RelativeLayout.__init__(self, **args)
		self.lastTouch = None
		self.tiles = []
		self.viewPos = (50.7, -1.3)
		self.viewZoom = 12

		print "win size", Window.size

		self.GetViewBounds()

		t = TileWidget(size=(200,200), pos=(50,50))
		self.add_widget(t)
		self.tiles.append(t)
		t2 = TileWidget(size=(200,200), pos=(250,50))
		self.add_widget(t2)
		self.tiles.append(t2)

		self.bind(pos=self.update_graphics_pos,
			size=self.update_graphics_size)

	def on_touch_down(self, touch):
		print "layer touch"
		self.lastTouch = touch.pos

	def on_touch_move(self, touch):
		relativeMove = (touch.pos[0] - self.lastTouch[0], touch.pos[1] - self.lastTouch[1])
		self.lastTouch = touch.pos

		for ti in self.tiles:
			ti.pos = (ti.pos[0]+relativeMove[0], ti.pos[1]+relativeMove[1])

	def GetViewBounds(self):
		tilex, tiley = slippy.deg2num(self.viewPos[0], self.viewPos[1], self.viewZoom)
		print "centre tile pos", tilex, tiley
		print "layout size", self.size
		print "layout size", self.size_hint
		#print slippy.num2deg(tilex, tiley, self.viewZoom)
		#print slippy.num2deg(tilex+1, tiley, self.viewZoom)
		#print slippy.num2deg(tilex, tiley+1, self.viewZoom)

	def update_graphics_size(self, instance, value):
		print "layout update_graphics_size", self.size_hint, self.size

	def update_graphics_pos(self, instance, value):
		pass

class KivMapApp(App):

	def __init__(self, **args):

		App.__init__(self, **args)

	def build(self):
		return MapLayer(size_hint=(1., 1.))


if __name__ == '__main__':
	KivMapApp().run()

