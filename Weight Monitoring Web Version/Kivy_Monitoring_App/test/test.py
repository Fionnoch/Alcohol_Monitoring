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
from kivy.core.window import Window
from kivy.config import Config

import win32gui
import win32con
import win32api

# Get the window
handle = win32gui.FindWindow(None, "My")

# Make it a layered window
#win32gui.SetWindowLong(handle, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(self.handle, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

# make it transparent (alpha between 0 and 255)
#win32gui.SetLayeredWindowAttributes(handle, win32api.RGB(0, 0, 0), alpha, win32con.LWA_ALPHA)


class MyGrid(Widget): #creates apps layout and contents
        #declaire global variables to pass to and from .kv file. note the variables names must be the same between the 2 files 
        name = ObjectProperty(None) #initialise as none and then after reading the .kv file it will populate it 
        email = ObjectProperty(None)
        
        def btn(self): #function btn which occurs. it needs to be in here 
            print ("name: ", self.name.text, " email: ", self.email.text)
            self.name.text = ""
            self.email.text = ""

class MyApp(App): #creates the app
    def build(self):
        return MyGrid()

if __name__ == '__main__': #runs the app 
    MyApp().run()