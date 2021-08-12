#kivy_venv\Scripts\activate

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.network.urlrequest import UrlRequest
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

from kivy_garden.graph import Graph
from kivy_garden.graph import MeshLinePlot

from functools import partial
import csv
import numpy as np
from numpy import genfromtxt
#import pandas as pd
from io import StringIO
from datetime import datetime
from datetime import date, timedelta

from math import sin

num_of_buttons = 3

kivy.require("1.11.1")

search_url = ('http://beehivemonitor.000webhostapp.com/Micro/Brewing/Weight_Ref_Retrieve.php')
Brew_table_list = list()
Brew_table_matrix = np.zeros(shape=(2,2)) #preallocate brew table incase user selects a batch number without selecting update first 
unique_batch_numbers = tuple() # a list of all the batch number with no repitition
unique_brew_names = tuple()

#graph_display = ObjectProperty(None)
brew_name = ObjectProperty(None) #initialise as none and then after reading the .kv file it will populate it 
batch_num = ObjectProperty(None)  

class MainWindow(Screen):
    def presses_brew_name(self):
        print("pressed button")
    
    def presses_batch_num(self):
        print("pressed batch num")
        #print(Brew_table_matrix[:,1])

    def pressed_update(self):
        print("pressed update button")
        print(search_url)
        self.request = UrlRequest(search_url, on_success=partial(self.Brew_info_update))

    def Brew_info_update(self, *args):
        print("successfully read from site")
        Brew_table_str = self.request.result #collect result as string

        temp_Brew_table_list = Brew_table_str.splitlines() #split string based on newline (/n)
        Brew_table_list = list()
        for i in range(len(temp_Brew_table_list)): #split each element up and append it while keeping the row structure
            temp = temp_Brew_table_list[i].split(',')
            Brew_table_list.append(temp)

        global Brew_table_matrix
        Brew_table_matrix = np.array(Brew_table_list)# store in numpy array as it is easier to control with syntax
        global unique_batch_numbers
        unique_batch_numbers = np.unique(Brew_table_matrix[:,1])
        global unique_brew_names 
        unique_brew_names = np.unique(Brew_table_matrix[:,0])
        #print(Brew_table_matrix)
        #print (Brew_table_matrix[:,0])

    def pressed_analyse(self): #this function will be used to check the if the parameters have a value
        print("pressed analyse")
        print("brew name = ", Brew_name)
        print("brew num = ", int(batch_num))
        print('start date and time (H:min d/m/y) = %d:%d %d/%d/%d' %(start_hour, start_minute, start_day, start_month, start_year))
        print('end date and time (H:min d/m/y) = %d:%d %d/%d/%d' %(end_hour, end_minute, end_day, end_month, end_year))

class BatchNumWindow(Screen):
    #global brew_name #= ObjectProperty(None) #initialise as none and then after reading the .kv file it will populate it 
    #batch_num = ObjectProperty(None)  

    def on_enter(self): #goal of this function is to create a box for each batch number
        
        print(unique_batch_numbers)

        for i in range(len(unique_batch_numbers)): #as buttons are dynamically allocated all stylings for the buttons need to be done here 
            button_name = "button" + str(i)
            setattr(self, button_name, Button( #NB normal syntax would be self.button=Button(parameters) however as we are looping to create buttons, each button needs a unique name which can only be done by using the setattr syntax
                                                text= str(unique_batch_numbers[i]), #will be replaced by batch numbers
                                                on_press = self.after_selected))
            self.ids.Batch_num_layout.add_widget(getattr(self,button_name))

    def after_selected(self, instance):
        
        ##save the selected buttons
        global batch_num
        batch_num = str(instance.text)
        batch_num = batch_num.strip(" ")
        print("pressed button = ", batch_num) #show the text of the pressed button
        #print(self.batch_num.text) #trying to find the name of button to display which button we have selected 
        
        ##switch screens 
        self.manager.current = 'main'
        
        ##clear page 
        
        for i in range(len(unique_batch_numbers)):
            button_name = "button" + str(i)
            self.ids.Batch_num_layout.remove_widget(getattr(self, button_name))

class BrewNameWindow(Screen):
    def on_enter(self): #goal of this function is to create a box for each batch number
        
        print(unique_brew_names)

        for i in range(len(unique_brew_names)): #as buttons are dynamically allocated all stylings for the buttons need to be done here 
            button_name = "button" + str(i)
            setattr(self, button_name, Button( #NB normal syntax would be self.button=Button(parameters) however as we are looping to create buttons, each button needs a unique name which can only be done by using the setattr syntax
                                                    text=str(unique_brew_names[i]), #will be replaced by batch numbers
                                                    on_press = self.after_selected))
            self.ids.Brew_name_layout.add_widget(getattr(self,button_name)) #in the kivy file under the brew name screen there is a layout with the id Brew_name_layout to which we are adding this 

    def after_selected(self, instance):
        ##save the selected button
        global Brew_name
        Brew_name = str(instance.text)
        print("pressed button = ", Brew_name)

        ##switch back to main screen 
        self.manager.current = 'main'
        
        ##clear page of old buttons so they dont stack when the button is called again
        for i in range(len(unique_brew_names)):
            button_name = "button" + str(i)
            self.ids.Brew_name_layout.remove_widget(getattr(self, button_name))

class DateTimeEditor(Widget):
    
    def __init__(self):
        self.day_31 = [1, 3, 5, 7, 8, 10, 12]
        self.day_30 = [4, 6, 9, 11]
        self.day_29 = [2]

    def Day_plus(self, current_num, start_end):
        print ("entered day analysis function" )
        date_limits = DateTimeEditor()
        if start_end == "S":
            month = int(self.ids.input_start_month.text)
        elif start_end == "E":
            month = int(self.ids.input_end_month.text)
        print ("month = ", month)
        if (month in date_limits.day_31):
            print("31 day month")
            if (current_num >= 31):
                current_num = 0
        elif(month in date_limits.day_30):
            print("30 day month")
            if (current_num >= 30):
                current_num = 0
        elif(month in date_limits.day_29):
            print("29 day month")
            if (current_num >= 29):
                current_num = 0  
        current_num = current_num+1
        return current_num

    def Day_minus(self, current_num, start_end):
        print ("entered day analysis function" )
        date_limits = DateTimeEditor()
        if start_end == "S":
            month = int(self.ids.input_start_month.text)
        elif start_end == "E":
            month = int(self.ids.input_end_month.text)
        print ("month = ", month)
        if (current_num <= 1):
            if (month in date_limits.day_31):
                print("31 day month")
                current_num = 32 #make it 1 number larger than the max that it 
            elif (month in date_limits.day_30):
                print("30 day month")
                current_num = 31
            elif (month in date_limits.day_29):
                print("29 day month")
                current_num = 30
        
        current_num = current_num-1
        return current_num

    def Month_plus(self, current_num, start_end):
        print ("entered month analysis function" )
        date_limits = DateTimeEditor()
        day = int(self.ids.input_start_day.text)
        print ("day = ", day)
        if current_num >= 12:
            current_num = 0
        new_num = current_num + 1

        if (new_num in date_limits.day_30) and (day > 30):  
            self.ids.input_start_day.text = "30"
        if (new_num in date_limits.day_29) and (day > 29):  
            self.ids.input_start_day.text = "29"   
        #no need for day_31 as it is the highest
        return new_num

    def Month_minus(self, current_num, start_end):
        print ("entered month analysis function" )
        date_limits = DateTimeEditor()
        day = int(self.ids.input_start_day.text)
        print ("day = ", day)
        if current_num <= 1:
            current_num = 13
        new_num = current_num - 1

        if (new_num in date_limits.day_30) and (day > 30):  
            self.ids.input_start_day.text = "30"
        if (new_num in date_limits.day_29) and (day > 29):  
            self.ids.input_start_day.text = "29"
        return new_num

    def Year_plus(self, current_num, start_end):
        new_num = current_num + 1
        return new_num

    def Year_minus(self, current_num, start_end):
        new_num = current_num - 1
        return new_num

    def Hour_plus(self, current_num, start_end):
        if current_num >= 23:
            current_num = -1    
        new_num = current_num + 1
        return new_num 

    def Hour_minus(self, current_num, start_end):
        if current_num <= 0:
            current_num = 24    
        new_num = current_num - 1
        return new_num 

    def Minute_plus(self, current_num, start_end):
        print ("entered minute plus function" )
        if current_num > 54:
            current_num = -5
        new_num = current_num+5 #skip forward 5 minutes to save time
        return new_num

    def Minute_minus(self, current_num, start_end):
        print ("entered minute minus function" )
        if current_num < 5:
            current_num = 60 
        new_num = current_num-5 #skip forward 5 minutes to save time
        return new_num

class TimeSelectWindow(Screen): #create the widget

    def IncreaseNum(self, text_box_to_change, num_type, start_end): #function which inputs the id of the label to be changed and changes is 
        temp_variable = getattr(self,text_box_to_change)
        current_num = int(temp_variable.text)
        
        new_num = { #switch statement. uses dictionary to refer number type to the correct function
            "D" : lambda current_num: DateTimeEditor.Day_plus(self, current_num, start_end),
            "M" : lambda current_num: DateTimeEditor.Month_plus(self, current_num, start_end),
            "Y" : lambda current_num: DateTimeEditor.Year_plus(self, current_num, start_end),
            "H" : lambda current_num: DateTimeEditor.Hour_plus(self, current_num, start_end),
            "Min" : lambda current_num: DateTimeEditor.Minute_plus(self, current_num, start_end)
        } [num_type] (current_num)    
        
        temp_variable.text = str(new_num)
        print("current number is ", current_num) 
        print("new number is ", new_num)

    def DecreaseNum(self, text_box_to_change, num_type, start_end):
        temp_variable = getattr(self,text_box_to_change)
        current_num = int(temp_variable.text)

        new_num = { #switch statement. uses dictionary to refer number type to the correct function
            "D" : lambda current_num: DateTimeEditor.Day_minus(self, current_num, start_end),
            "M" : lambda current_num: DateTimeEditor.Month_minus(self, current_num, start_end),
            "Y" : lambda current_num: DateTimeEditor.Year_minus(self, current_num, start_end),
            "H" : lambda current_num: DateTimeEditor.Hour_minus(self, current_num, start_end),
            "Min" : lambda current_num: DateTimeEditor.Minute_minus(self, current_num, start_end)
        } [num_type] (current_num)

        temp_variable.text = str(new_num)
        print("current number is ", current_num) 
        print("new number is ", new_num)

    def Submit_datetimes(self):
        global start_day, start_month, start_year, start_minute, start_hour #save items to global memory before they were in temporary memory as they kept changing   
        global end_day, end_month, end_year, end_minute, end_hour
        start_day = int(self.input_start_day.text) #convert to intigers 
        start_month = int(self.input_start_month.text)
        start_year = int(self.input_start_year.text)
        start_minute = int(self.input_start_minute.text)
        start_hour = int(self.input_start_hour.text)

        end_day = int(self.input_end_day.text) #convert to intigers 
        end_month = int(self.input_end_month.text)
        end_year = int(self.input_end_year.text)
        end_minute = int(self.input_end_minute.text)
        end_hour = int(self.input_end_hour.text)

        #print(start_day)
        print('start date and time (H:min d/m/y) = %d:%d %d/%d/%d' %(start_hour, start_minute, start_day, start_month, start_year))
        print('end date and time (H:min d/m/y) = %d:%d %d/%d/%d' %(end_hour, end_minute, end_day, end_month, end_year))

class TimeSeriesGraph(Graph):
    
    def __init__(self, x_date_labels, date_label_format = '%b', _with_stencilbuffer = False, **kwargs):
        self.x_date_labels = x_date_labels
        self._date_label_format = date_label_format
        self._with_stencilbuffer = _with_stencilbuffer
        kwargs["xmin"] = 0
        kwargs["xmax"] = len(self.x_date_labels) - 1
        super(TimeSeriesGraph, self).__init__(**kwargs)

    def _get_ticks(self, major, minor, log, s_min, s_max):
        if major == 'month':
            points_major = []
            m = self.x_date_labels[0].month
            for i in range(len(self.x_date_labels)):
                if self.x_date_labels[i].month != m:
                    m = self.x_date_labels[i].month
                    points_major.append(float(i))

            points_minor = []
        else:
            points_major, points_minor = super(TimeSeriesGraph, self)._get_ticks(major, minor, log, s_min, s_max)

        return points_major, points_minor

    def _update_labels(self):
        xlabel = self._xlabel
        ylabel = self._ylabel
        x = self.x
        y = self.y
        width = self.width
        height = self.height
        padding = self.padding
        x_next = padding + x
        y_next = padding + y
        xextent = width + x
        yextent = height + y
        ymin = self.ymin
        ymax = self.ymax
        xmin = self.xmin
        precision = self.precision
        x_overlap = False
        y_overlap = False
        # set up x and y axis labels
        if xlabel:
            xlabel.text = self.xlabel
            xlabel.texture_update()
            xlabel.size = xlabel.texture_size
            xlabel.pos = int(x + width / 2. - xlabel.width / 2.), int(padding + y)
            y_next += padding + xlabel.height
        if ylabel:
            ylabel.text = self.ylabel
            ylabel.texture_update()
            ylabel.size = ylabel.texture_size
            ylabel.x = padding + x - (ylabel.width / 2. - ylabel.height / 2.)
            x_next += padding + ylabel.height
        xpoints = self._ticks_majorx
        xlabels = self._x_grid_label
        xlabel_grid = self.x_grid_label
        ylabel_grid = self.y_grid_label
        ypoints = self._ticks_majory
        ylabels = self._y_grid_label
        # now x and y tick mark labels
        if len(ylabels) and ylabel_grid:
            # horizontal size of the largest tick label, to have enough room
            funcexp = exp10 if self.ylog else identity
            funclog = log10 if self.ylog else identity
            ylabels[0].text = precision % funcexp(ypoints[0])
            ylabels[0].texture_update()
            y1 = ylabels[0].texture_size
            y_start = y_next + (padding + y1[1] if len(xlabels) and xlabel_grid
                                else 0) + \
                               (padding + y1[1] if not y_next else 0)
            yextent = y + height - padding - y1[1] / 2.

            ymin = funclog(ymin)
            ratio = (yextent - y_start) / float(funclog(ymax) - ymin)
            y_start -= y1[1] / 2.
            y1 = y1[0]
            for k in range(len(ylabels)):
                ylabels[k].text = precision % funcexp(ypoints[k])
                ylabels[k].texture_update()
                ylabels[k].size = ylabels[k].texture_size
                y1 = max(y1, ylabels[k].texture_size[0])
                ylabels[k].pos = tuple(map(int, (x_next, y_start +
                                                 (ypoints[k] - ymin) * ratio)))
            if len(ylabels) > 1 and ylabels[0].top > ylabels[1].y:
                y_overlap = True
            else:
                x_next += y1 + padding
        if len(xlabels) and xlabel_grid:
            funcexp = exp10 if self.xlog else identity
            funclog = log10 if self.xlog else identity
            # find the distance from the end that'll fit the last tick label
            xlabels[0].text = precision % funcexp(xpoints[-1])
            xlabels[0].texture_update()
            xextent = x + width - xlabels[0].texture_size[0] / 2. - padding
            # find the distance from the start that'll fit the first tick label
            if not x_next:
                xlabels[0].text = precision % funcexp(xpoints[0])
                xlabels[0].texture_update()
                x_next = padding + xlabels[0].texture_size[0] / 2.
            xmin = funclog(xmin)
            ratio = (xextent - x_next) / float(funclog(self.xmax) - xmin)
            right = -1
            for k in range(len(xlabels)):
                xlabels[k].text = self.x_date_labels[int(xpoints[k])].strftime(self._date_label_format)
                # update the size so we can center the labels on ticks
                xlabels[k].texture_update()
                xlabels[k].size = xlabels[k].texture_size
                xlabels[k].pos = tuple(map(int, (x_next + (xpoints[k] - xmin)
                    * ratio - xlabels[k].texture_size[0] / 2., y_next)))
                if xlabels[k].x < right:
                    x_overlap = True
                    break
                right = xlabels[k].right
            if not x_overlap:
                y_next += padding + xlabels[0].texture_size[1]
        # now re-center the x and y axis labels
        if xlabel:
            xlabel.x = int(x_next + (xextent - x_next) / 2. - xlabel.width / 2.)
        if ylabel:
            ylabel.y = int(y_next + (yextent - y_next) / 2. - ylabel.height / 2.)
            t = Matrix().translate(ylabel.center[0], ylabel.center[1], 0)
            t = t.multiply(Matrix().rotate(-radians(270), 0, 0, 1))
            ylabel.transform = t.multiply(
                Matrix().translate(
                    -int(ylabel.center_x),
                    -int(ylabel.center_y),
                    0))
        if x_overlap:
            for k in range(len(xlabels)):
                xlabels[k].text = ''
        if y_overlap:
            for k in range(len(ylabels)):
                ylabels[k].text = ''
        return x_next - x, y_next - y, xextent - x, yextent - y



class AnalysisWindow(Screen):

    def download_data(self):
        #print("pressed analyse")
        #print("brew name = ", Brew_name)
        #print("brew num = ", int(batch_num))
        #print('start date and time (H:min d/m/y) = %d:%d %d/%d/%d' %(start_hour, start_minute, start_day, start_month, start_year))
        #print('end date and time (H:min d/m/y) = %d:%d %d/%d/%d' %(end_hour, end_minute, end_day, end_month, end_year))
        start_time_format = ('%d:%d:%d' %(start_hour, start_minute, 00))
        end_time_format = ('%d:%d:%d' %(end_hour, end_minute, 00))
        start_date_format = ('%d-%d-%d' %(start_day, start_month, start_year))
        end_date_format = ('%d-%d-%d' %(end_day, end_month, end_year))
        #e.g http://beehivemonitor.000webhostapp.com/Micro/Brewing/Weight_Retrieve.php?           Brew_ID=Mead         &Batch_ID=2              &start_date=01-05-2020          &start_time=14:02:15            &end_date=22-05-2020        &end_time=19:05:00
        pull_data_url = "http://beehivemonitor.000webhostapp.com/Micro/Brewing/Weight_Retrieve.php?"+"Brew_ID="+Brew_name+"&Batch_ID="+batch_num+"&start_date="+start_date_format+"&start_time="+ start_time_format+"&end_date="+end_date_format+"&end_time="+end_time_format
        print(pull_data_url)
        #UrlRequest(pull_data_url, on_success=partial(self.graph_function))
        self.brew_data_temp = UrlRequest(pull_data_url, on_success=partial(self.graph_function))
        #data = pd.read_csv(pull_data_url, sep=',', escapechar='<br>')
        #print(data)
        #AnalysisWindow.graph_function(self)

    graph_display = ObjectProperty(None)

    def graph_function(self, *args):
        print("successfully read from site")
        Brew_data_str = self.brew_data_temp.result #collect result as string
        print ("data from site:")
        temp = StringIO(Brew_data_str.replace('<br>', '\n'))
        #datatypes = ([('Timestamp', '<f8'), ('Weight', '<f8'), ('Volume', '<f8'), ('Density', '<f8'), ('Current_SG', '<f8'), ('Target_SG', '<f8'), ('Initial_SG', '<f8'), ('Alcohol_Percent', '<f8'), ('Comment', '<s8'), ('f0', '<s8')])
        Brew_data_np = np.genfromtxt(temp, delimiter=",", names = True, dtype = ([('Timestamp', '<i8'), ('Weight', '<f8'), ('Volume', '<f8'), ('Density', '<f8'), ('Current_SG', '<f8'), ('Target_SG', '<f8'), ('Initial_SG', '<f8'), ('Alcohol_Percent', '<f8'), ('Comment', '<S8'), ('f0', '<S8')]))
        print(Brew_data_np)
        
        #create the graph
        print("entered function")

        print(Brew_data_np.dtype.names)
        x_label = Brew_data_np.dtype.names[0]
        y_label = Brew_data_np.dtype.names[7]

        #print("test date = ", datetime.utcfromtimestamp(Brew_data_np[x_label][0]).strftime('%Y-%m-%d %H:%M:%S'))
        #test_time = datetime.utcfromtimestamp(Brew_data_np[x_label]).strftime('%Y-%m-%d %H:%M:%S')
        test_time = list()
        for i in range(len(Brew_data_np["Timestamp"])):
            test_time.append( datetime.fromtimestamp(Brew_data_np["Timestamp"][i]) )
            
        #datetime.utcfromtimestamp(Brew_data_np[x_label][i]).strftime('%Y-%m-%d %H:%M:%S')
        
        print(test_time)

        #datetime.fromtimestamp(timestamp)

        self.graph_display.xlabel = Brew_data_np.dtype.names[0]
        self.graph_display.ylabel = y_label # Brew_data_np.dtype.names[7]
        self.graph_display.xmin= int(Brew_data_np[x_label][0])
        self.graph_display.xmax= int(Brew_data_np[x_label][-1]) 
        self.graph_display.ymin= float(min(Brew_data_np[y_label]))
        self.graph_display.ymax= float(max(Brew_data_np[y_label]))
        #self.graph_display.x_grid=True
        #self.graph_display.y_grid=True
        plot = MeshLinePlot(color=[1, 0, 0, 1])

        #points_to_plot = [(Brew_data_np["Timestamp"][i], Brew_data_np["Alcohol_Percent"][i]) for i in range(len(Brew_data_np["Timestamp"]))]
        #points_to_plot = [(test_time[i], Brew_data_np["Alcohol_Percent"][i]) for i in range(len(Brew_data_np["Timestamp"]))]
        #points_to_plot = zip(Brew_data_np["Timestamp"], Brew_data_np["Alcohol_Percent"])
        points_to_plot = zip(Brew_data_np["Timestamp"], Brew_data_np["Alcohol_Percent"])
        print(points_to_plot)

        plot.points = points_to_plot
        #self.graph.add_plot(plot)

        #[(x, sin(x)*1000) for x in range(0, 100)]

        self.ids.graph_display.add_plot(plot)
        print("finished plot")
        #self.ids.graph_display.add_widget(self.graph)
        #.ids.graph_display

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("brewingtester.kv") #needs to be right before myMainApp 

class MyMainApp(App):
    def build(self):
        return kv

#    def _finish_init(self, dt):
#        self.graph = self.ids.Graph_layout
        #AnalysisWindow

if __name__ == "__main__":
    MyMainApp().run()