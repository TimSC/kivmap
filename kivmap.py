from kivy.app import App
from kivy.core.window import Window
import random, layer

class KivMapApp(App):

	def __init__(self, **args):

		App.__init__(self, **args)

	def build(self):
		return layer.MapLayer(size_hint=(1., 1.))


if __name__ == '__main__':
	KivMapApp().run()

