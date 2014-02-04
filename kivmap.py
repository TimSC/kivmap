from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line, Rectangle
import random

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
		print "update_graphics_pos"
		for obj in self.objs:
			obj.pos = value

	def update_graphics_size(self, instance, value):
		print "update_graphics_size"

class MapLayer(FloatLayout):
	def __init__(self, **args):
		FloatLayout.__init__(self, **args)
		self.lastTouch = None
		self.tiles = []

		t = TileWidget(size=(200,200), pos=(50,50))
		self.add_widget(t)
		self.tiles.append(t)
		t2 = TileWidget(size=(200,200), pos=(250,50))
		self.add_widget(t2)
		self.tiles.append(t2)

	def on_touch_down(self, touch):
		print "layer touch"
		self.lastTouch = touch.pos

	def on_touch_move(self, touch):
		relativeMove = (touch.pos[0] - self.lastTouch[0], touch.pos[1] - self.lastTouch[1])
		self.lastTouch = touch.pos
		print relativeMove

		for ti in self.tiles:
			print ti.pos
			ti.x = ti.pos[0]+relativeMove[0]
			ti.y = ti.pos[1]+relativeMove[1]



class KivMapApp(App):

	def build(self):

		return MapLayer(size=(1.,1.))

if __name__ == '__main__':
	KivMapApp().run()
