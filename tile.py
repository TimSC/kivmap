from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line, Rectangle

class TileWidget(Widget):

	def __init__(self, **args):
		Widget.__init__(self, **args)
		self.objs = []
		self.tileNum = (None, None)

		with self.canvas:
			Color(1., 1., 0)
			self.objs.append(Rectangle(pos=self.pos, size=(self.width, self.height)))
			Color(0, 0.7, 0)
			self.objs.append(Ellipse(pos=self.pos, size=self.size))
			Color(0, 0, 0.4)
			self.label = Label(pos=self.pos, text="test")
			self.objs.append(self.label)

		self.bind(pos=self.update_graphics_pos,
			size=self.update_graphics_size)
	
	def SetTileNum(self, x, y):
		self.label.text = "{0}, {1}".format(x, y)

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

