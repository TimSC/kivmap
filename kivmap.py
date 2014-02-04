from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line, Rectangle
import random

class TileWidget(Widget):

	def __init__(self, **args):
		Widget.__init__(self, **args)

		with self.canvas:
			Color(1., 1., 0)
			Rectangle(pos=self.pos, size=(self.width, self.height))
			Color(0, 0.7, 0)
			self.rect = Ellipse(pos=self.pos, size=self.size)

	def on_touch_down(self, touch):
		with self.canvas:
			Color(1, 1, 0)
			d = 30.
			print (touch.x - d / 2, touch.y - d / 2)
			Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
			touch.ud['line'] = Line(points=(touch.x, touch.y))

	def on_touch_move(self, touch):
		touch.ud['line'].points += [touch.x, touch.y]

class MapLayer(Widget):
	def __init__(self, **args):
		Widget.__init__(self, **args)


	def on_touch_down(self, touch):
		pass

	def on_touch_move(self, touch):
		pass

class KivMapApp(App):

	def build(self):
		layout = FloatLayout(size=(1.,1.))
		t = TileWidget(size=(200,200), pos=(50,50))
		layout.add_widget(t)
		t2 = TileWidget(size=(200,200), pos=(250,50))
		layout.add_widget(t2)
		return layout

if __name__ == '__main__':
	KivMapApp().run()
