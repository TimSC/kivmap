from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.uix.stencilview import StencilView
import slippy

class TileWidget(Scatter):
	def __init__(self, **args):
		Scatter.__init__(self, **args)
		self.do_rotation = False
		self.do_scale = False
		self.do_translation = False

		self.bind(pos=self.update_graphics_pos,
			size=self.update_graphics_size)

		self.tileView = TileView(size=(512, 512))
		self.add_widget(self.tileView)
		self.drawDone = False

	def update_graphics_pos(self, instance, value):
		pass

	def update_graphics_size(self, instance, value):
		pass

	def SetMap(self, map):
		self.tileView.SetMap(map)

	def SetTileNum(self, x, y, zoom):
		self.tileView.SetTileNum(x, y, zoom)

	def IsDrawDone(self):
		return self.drawDone

	def Draw(self, hints={}):
		self.tileView.Draw(hints)
		self.drawDone = True

class TileView(StencilView):

	def __init__(self, **args):
		StencilView.__init__(self, **args)

		self.objs = []
		self.tileNum = (None, None)
		self.tileZoom = None

		with self.canvas:
			Color(1., 1., 0)
			self.objs.append(Rectangle(pos=(0., 0), size=(self.width, self.height)))
			Color(0, 0.7, 0)
			self.objs.append(Ellipse(pos=(0., 0), size=self.size))
			Color(0, 0, 0.4)
			self.label = Label(pos=(0., 0), text="test")
			self.objs.append(self.label)

		self.bind(pos=self.update_graphics_pos,
			size=self.update_graphics_size)
	
	def SetTileNum(self, x, y, zoom):
		self.tileNum = (x, y)
		self.tileZoom = zoom
		self.label.text = "[color=0000ff]{0}, {1}, {2}[/color]".format(x, y, zoom)
		self.label.markup = True

	def on_touch_down(self, touch):
		pass

	def on_touch_move(self, touch):
		pass

	def update_graphics_pos(self, instance, value):
		#for obj in self.objs:
		#	obj.pos = value
		pass

	def update_graphics_size(self, instance, value):
		#print "widget update_graphics_size"
		pass

	def SetMap(self, map):
		self.map = map

	def Draw(self, hints={}):
		if self.map is not None:
			tl = slippy.num2deg(self.tileNum[0], self.tileNum[1], self.tileZoom)
			br = slippy.num2deg(self.tileNum[0]+1, self.tileNum[1]+1, self.tileZoom)
			proj = slippy.TileProj(self.tileNum[0], self.tileNum[1], self.tileZoom, self.size[0], self.size[1])
			self.map.Draw((tl[1], br[0], br[1], tl[0]), self.tileZoom, hints, self.DrawCallback, proj.Proj)
			#bounds left,bottom,right,top

	def DrawCallback(self, obj):
		self.objs.append(obj)
		self.canvas.add(obj)

