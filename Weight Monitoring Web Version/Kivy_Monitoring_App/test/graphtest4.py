from math import sin
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


class RootWidget(Screen):
    #_touch_count = NumericProperty(0)

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.plot = MeshLinePlot(color=[.5, .5, 1, 1])


        self.graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
                           x_ticks_major=25, y_ticks_major=1,
                           y_grid_label=True, x_grid_label=True, padding=5,
                           x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-1000, ymax=1000)

        plot = MeshLinePlot(color=[1, 0, 0, 1])
        plot.points = [(x, sin(x)*1000) for x in range(0, 100)]
        self.graph.add_plot(plot)
        self.add_widget(self.graph)


class GraphDemox(App):

    def build(self):
        #return Builder.load_file("GraphTestx.kv")
        return RootWidget()


if __name__ == "__main__":
    GraphDemox().run()