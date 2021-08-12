import kivy
from kivy.app import App 
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

#import kivy.graphics.instructions.VertexInstruction
#from kivy.graphics.instructions.VertexInstruction import vertex_instructions
#from kivy.graphics.vertex_instructions
#from kivy.graphics.vertex
import kivy.graphics

from kivy.graphics.vertex_instructions.triangle import triangle

class MyWidget(Button):
    
    triangle = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        with self.canvas:
            self.triangle = Triangle(points=[0,0, 100,100, 200,0])

class shapetest(App): #creates the app
    def build(self):
        return MyWidget()

if __name__ == '__main__': #runs the app 
    shapetest().run()