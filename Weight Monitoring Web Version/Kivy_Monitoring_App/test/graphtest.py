import sys
from math import sin
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.app import App

from kivy.uix.widget import Widget
from kivy_garden.graph import Graph, MeshLinePlot


class SetGraph(Widget):
    #def __init__(self, **kwargs):
    #    super(SetGraph, self).__init__(**kwargs)

    def update_graph(self):
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        plot.points = [(x, sin(x / 10.0)) for x in range(0, 101)]
        App.get_running_app().root.ids.graph_test.add_plot(plot)

def press_button(self):
     print("pressed button")


class GraphLayoutApp(App):
    
    def build(self):
        #ids = self.root.ids
        #ids.g_test.update_graph()
        return Builder.load_file("GraphTest.kv")

    #def on_start(self):
    #    """On Start"""
    #    ids = self.root.ids
    #    ids.g_test.update_graph()


if __name__ == "__main__":
    GraphLayoutApp().run()