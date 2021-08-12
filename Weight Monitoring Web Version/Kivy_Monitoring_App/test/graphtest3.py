from math import sin
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty


class RootWidget(Screen):
    _touch_count = NumericProperty(0)

    graph_display = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        #create the graph
        #self.graph = Graph()
        #self.graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
        #                   x_ticks_major=25, y_ticks_major=1,
        #                   y_grid_label=True, x_grid_label=True, padding=5,
        #                   x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-1000, ymax=1000)
        self.graph_display.xlabel='test'
        self.graph_display.ylabel='test'
        self.graph_display.xmin=-0 
        self.graph_display.xmax=100 
        self.graph_display.ymin=-1 
        self.graph_display.ymax=1
        #self.graph_display.x_grid=True
        #self.graph_display.y_grid=True
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
        #self.graph.add_plot(plot)
        self.ids.graph_display.add_plot(plot)
        #self.ids.graph_display.add_widget(self.graph)
        #.ids.graph_display


class GraphDemo(App):

    def build(self):
        #return Builder.load_file("GraphTestx.kv")
        return RootWidget()


if __name__ == "__main__":
    GraphDemo().run()