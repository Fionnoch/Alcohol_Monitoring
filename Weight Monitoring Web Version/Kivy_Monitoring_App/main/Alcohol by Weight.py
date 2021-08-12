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
from kivy.uix.popup import Popup
from kivy.uix.label import Label

import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.dates as mpl_dates

from functools import partial
import csv
import pandas as pd
from io import StringIO
from datetime import datetime
from datetime import date, timedelta

#from time import sleep

global num_of_batch_num_buttons
num_of_batch_num_buttons = 0

global num_of_brew_name_buttons
num_of_brew_name_buttons = 0

global Selected_brew_name
Selected_brew_name = False

global Selected_batch_num
Selected_batch_num = False

global Selected_dates
Selected_dates = False

global Pressed_update
Pressed_update = False

global filtered_batch_nums

global Brew_name
Brew_name = ""
global batch_num
batch_num = 0

global unique_brew_names #create blank dataframe incase user selects brew name button before data is loaded
unique_brew_names = pd.DataFrame() 

global unique_batch_numbers
unique_batch_numbers = pd.DataFrame() 

kivy.require("1.11.1")

search_url = ('http://beehivemonitor.000webhostapp.com/Micro/Brewing/Weight_Ref_Retrieve.php')

def connection_error_popup(self, *args): 
    #windowmanager.current_screen = "BatchNumWindow"
    dismiss_button = Button(text='Could not connect, check internet connection.')
    
    global screen_height
    global screen_width

    popup = Popup(title='Connection Error',
        content=dismiss_button,
        size_hint=(None, None), 
        size=(screen_width*.8, screen_height*.8), 
        auto_dismiss=True)
    
    dismiss_button.bind(on_press=popup.dismiss)
    
    popup.open()

    #ScreenManager.current_screen = "MainScreen"

def selection_error_popup(self):
    #WindowManager.current_screen = "BatchNumWindow"
    dismiss_button = Button(text='Brew Name, Batch ID, Time combination not found \n Please reselect.', halign='center')

    popup = Popup(title='Combination Error',
        content=dismiss_button,
        size_hint=(None, None), 
        size=(self.width*.8, self.height*.8), 
        auto_dismiss=True)
    
    dismiss_button.bind(on_press=popup.dismiss)
    
    popup.open()

def not_updated(self):
    #WindowManager.current = "BatchNumWindow"
    dismiss_button = Button(text='No info downloaded. \nPlease press Update.')

    popup = Popup(title='Update Error',
        content=dismiss_button,
        size_hint=(None, None), 
        size=(self.width*.8, self.height*.8), 
        auto_dismiss=True)
    
    dismiss_button.bind(on_press=popup.dismiss)
    
    popup.open()

    

class MainWindow(Screen):
    def presses_brew_name(self):
        #print("pressed button")
        pass
    
    def presses_batch_num(self):
        #print("pressed batch num")
        #print(Brew_table_matrix[:,1])
        pass

    def pressed_update(self):
        #print("pressed update button")
        #print(search_url)
        global screen_height
        global screen_width
        screen_height = self.height
        screen_width = self.width
        self.request = UrlRequest(search_url, on_success=partial(self.Brew_info_update), on_error=partial(connection_error_popup))

    def Brew_info_update(self, *args):
        #print("successfully read from site")
        Brew_table_str = self.request.result #collect result as string

        temp_Brew_table_list = Brew_table_str.splitlines() #split string based on newline (/n)
        Brew_table_list = list()
        for i in range(len(temp_Brew_table_list)): #split each element up and append it while keeping the row structure
            temp = temp_Brew_table_list[i].split(',')
            Brew_table_list.append(temp)

        global Brew_table_matrix
        global pd_Brew_table_matrix
        Brew_table_matrix = pd.DataFrame(Brew_table_list, columns = ['Brew Name' , 'Brew ID', 'Start Time', 'Start Date', 'End Time', 'End Date', 'Null'])
        Brew_table_matrix['Brew ID'] = Brew_table_matrix['Brew ID'].astype('int')
        #pd_Brew_table_matrix = pd.DataFrame(Brew_table_list, columns = ['Brew Name' , 'Brew ID', 'Start Time', 'Start Date', 'End Time', 'End Date', 'Null'])
        #Brew_table_matrix = np.array(Brew_table_list)#, dtype = ['Brew name', 'Brew ID', 'Start Time', 'Start Date', 'End Time', 'End Date'])# store in numpy array as it is easier to control with syntax
        global unique_batch_numbers
        #unique_batch_numbers = pd_Brew_table_matrix['Brew ID'].drop_duplicates()
        unique_batch_numbers = Brew_table_matrix['Brew ID'].drop_duplicates()
        #unique_batch_numbers = np.unique(Brew_table_matrix[:,1])
        
        global unique_brew_names 
        #unique_brew_names = np.unique(Brew_table_matrix[:,0])
        #unique_brew_names = pd_Brew_table_matrix['Brew Name'].drop_duplicates()
        unique_brew_names = Brew_table_matrix['Brew Name'].drop_duplicates()

        global num_of_batch_num_buttons
        num_of_batch_num_buttons = len(unique_batch_numbers)

        global num_of_brew_name_buttons
        num_of_brew_name_buttons = len(unique_brew_names)

        global Pressed_update
        Pressed_update = True

    def pressed_analyse(self): #this function will be used to check the if the parameters have a value
        global Selected_brew_name
        global Selected_batch_num
        global Selected_dates
        global Pressed_update
        global Brew_name
        global batch_num

        if Pressed_update == True:
            correct_criteria =  Brew_table_matrix.loc[(Brew_table_matrix['Brew Name'] == Brew_name) & (Brew_table_matrix['Brew ID'] == int(batch_num))]

            if correct_criteria.empty == False and Selected_dates == True :
                #print("pressed analyse")
                #print("brew name = ", Brew_name)
                #print("brew num = ", int(batch_num))
                #print('start date and time (H:min d/m/y) = %d:%d %d/%d/%d' %(start_hour, start_minute, start_day, start_month, start_year))
                #print('end date and time (H:min d/m/y) = %d:%d %d/%d/%d' %(end_hour, end_minute, end_day, end_month, end_year))

                self.manager.current = 'Analysis'

            else: 
                self.manager.current = 'main' #MainWindow
                selection_error_popup(self)
        else:
            self.manager.current = 'main' #MainWindow
            not_updated(self)
          
    def UpdateDates(self):
        #print ("update dates and times for batch")

        global Selected_dates
        Selected_dates = True

        if Selected_brew_name == True & Selected_batch_num == True : 
            s_min = pd.to_timedelta(filtered_brew_table['Start Time']).dt.components['minutes']
            s_h = pd.to_timedelta(filtered_brew_table['Start Time']).dt.components['hours']

            s_d = pd.to_datetime(filtered_brew_table['Start Date']).dt.day
            s_m = pd.to_datetime(filtered_brew_table['Start Date']).dt.month
            s_y = pd.to_datetime(filtered_brew_table['Start Date']).dt.year

            e_min = pd.to_timedelta(filtered_brew_table['End Time']).dt.components['minutes']
            e_h = pd.to_timedelta(filtered_brew_table['End Time']).dt.components['hours']

            e_d = pd.to_datetime(filtered_brew_table['End Date']).dt.day
            e_m = pd.to_datetime(filtered_brew_table['End Date']).dt.month
            e_y = pd.to_datetime(filtered_brew_table['End Date']).dt.year

            self.manager.ids.TimeSelectWindow.ids.input_start_minute.text = str(int(s_min))
            self.manager.ids.TimeSelectWindow.ids.input_start_hour.text = str(int(s_h))

            self.manager.ids.TimeSelectWindow.ids.input_start_day.text = str(int(s_d))
            self.manager.ids.TimeSelectWindow.ids.input_start_month.text = str(int(s_m))
            self.manager.ids.TimeSelectWindow.ids.input_start_year.text = str(int(s_y))

            self.manager.ids.TimeSelectWindow.ids.input_end_minute.text = str(int(e_min))
            self.manager.ids.TimeSelectWindow.ids.input_end_hour.text = str(int(e_h))

            self.manager.ids.TimeSelectWindow.ids.input_end_day.text = str(int(e_d))
            self.manager.ids.TimeSelectWindow.ids.input_end_month.text = str(int(e_m))
            self.manager.ids.TimeSelectWindow.ids.input_end_year.text = str(int(e_y))

            #print start and end dates as the label. idea 
            #self.manager.ids.MainWindow.ids.start_end_date.text = str(filtered_brew_table['Start Time'])
            


        #if both criteria are filled 
        #   do nothing
        #else 
        #    check filtered brew table for dates and fill them into appropiate boxes
        #       reference screenmanager to access buttons 
        #       e.g self.manager.ids.MainWindow.ids.brew_name.text = Brew_name

class BrewNameWindow(Screen):

    def on_enter(self): #goal of this function is to create a box for each batch number
        
        #print(unique_brew_names) #the names are created in Brew_info_update 

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
        #print("pressed button = ", Brew_name)

        ##switch back to main screen 
        self.manager.current = 'main'
        
        global num_of_brew_name_buttons
        #print(num_of_brew_name_buttons)

        ##clear page of old buttons so they dont stack when the button is called again
        for i in range(num_of_brew_name_buttons):
            button_name = "button" + str(i)
            self.ids.Brew_name_layout.remove_widget(getattr(self, button_name))
            self.get_root_window

        # to do:
        # 1. update the names of the buttons on the mainscreen to show what the user selected.
        # 2. update the batch numbers to that it only displays numbers relevant to the selected brew name
        #print("Brew table matrix:")
        #print(Brew_table_matrix)
        
        global filtered_brew_table
        filtered_brew_table = Brew_table_matrix.loc[Brew_table_matrix['Brew Name'] == Brew_name]

        self.manager.ids.MainWindow.ids.brew_name.text = Brew_name #change button name to currently selected item

        global Selected_brew_name
        Selected_brew_name = True

    def reset_names(self):
        #print("entered brew name reset function")
        global num_of_brew_name_buttons
        #print ("num of buttons = ", num_of_brew_name_buttons)
        if num_of_brew_name_buttons > 0:
            #print("acknoledged that there are ", num_of_brew_name_buttons, " buttons")
            for i in range(num_of_brew_name_buttons):
                button_name = "button" + str(i)
                self.ids.Brew_name_layout.remove_widget(getattr(self, button_name))
        else:
            pass
            #print("no buttons")    

class BatchNumWindow(Screen): 

    def on_enter(self): #goal of this function is to create a box for each batch number
        
        #print(unique_batch_numbers)

        global filtered_brew_table

        #print ("num of buttons = ", num_of_batch_num_buttons)

        global brew_id_buttons

        if Selected_brew_name == True:
            brew_id_buttons = filtered_brew_table['Brew ID'].astype('int') 
        elif (Selected_brew_name == False):
            brew_id_buttons = unique_batch_numbers

        for i in brew_id_buttons: # range(len(unique_batch_numbers)): #as buttons are dynamically allocated all stylings for the buttons need to be done here 
            button_name = "button" + str(i)
            setattr(self, button_name, Button( #NB normal syntax would be self.button=Button(parameters) however as we are looping to create buttons, each button needs a unique name which can only be done by using the setattr syntax
                                                text= str(i), #will be replaced by batch numbers
                                                on_press = self.after_selected))
            self.ids.Batch_num_layout.add_widget(getattr(self,button_name))

    def after_selected(self, instance):
        
        ##save the selected buttons
        global batch_num
        batch_num = str(instance.text)
        batch_num = batch_num.strip(" ")
        #print("pressed button = ", batch_num) #show the text of the pressed button 
        
        ##switch screens 
        self.manager.current = 'main'
        
        ##clear page 

        for i in brew_id_buttons:
            button_name = "button" + str(i)
            self.ids.Batch_num_layout.remove_widget(getattr(self, button_name))

        self.manager.ids.MainWindow.ids.batch_num.text = batch_num #change button name to currently selected item

        global Selected_batch_num 
        Selected_batch_num = True

    def reset_numbers(self):
        #print("entered batch number reset function")
        global brew_id_buttons

        #print ("num of buttons = ", len(brew_id_buttons))
        if len(brew_id_buttons) > 0:
            #print("acknoledged that there are ", len(brew_id_buttons), " buttons")
            for i in brew_id_buttons:
                button_name = "button" + str(i)
                self.ids.Batch_num_layout.remove_widget(getattr(self, button_name))
        else:
            pass
            #print("no buttons")

class DateTimeEditor(Widget):
    
    def __init__(self):
        self.day_31 = [1, 3, 5, 7, 8, 10, 12]
        self.day_30 = [4, 6, 9, 11]
        self.day_29 = [2]

    def Day_plus(self, current_num, start_end):
        #print ("entered day analysis function" )
        date_limits = DateTimeEditor()
        if start_end == "S":
            month = int(self.ids.input_start_month.text)
        elif start_end == "E":
            month = int(self.ids.input_end_month.text)
        #print ("month = ", month)
        if (month in date_limits.day_31):
            #print("31 day month")
            if (current_num >= 31):
                current_num = 0
        elif(month in date_limits.day_30):
            #print("30 day month")
            if (current_num >= 30):
                current_num = 0
        elif(month in date_limits.day_29):
            #print("29 day month")
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
        #print ("month = ", month)
        if (current_num <= 1):
            if (month in date_limits.day_31):
                #print("31 day month")
                current_num = 32 #make it 1 number larger than the max that it 
            elif (month in date_limits.day_30):
                #print("30 day month")
                current_num = 31
            elif (month in date_limits.day_29):
                #print("29 day month")
                current_num = 30
        
        current_num = current_num-1
        return current_num

    def Month_plus(self, current_num, start_end):
        #print ("entered month analysis function" )
        date_limits = DateTimeEditor()
        day = int(self.ids.input_start_day.text)
        #print ("day = ", day)
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
        #print ("entered month analysis function" )
        date_limits = DateTimeEditor()
        day = int(self.ids.input_start_day.text)
        #print ("day = ", day)
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
        #print ("entered minute plus function" )
        if current_num > 54:
            current_num = -5
        new_num = current_num+5 #skip forward 5 minutes to save time
        return new_num

    def Minute_minus(self, current_num, start_end):
        #print ("entered minute minus function" )
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
        #print("current number is ", current_num) 
        #print("new number is ", new_num)

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
        #print("current number is ", current_num) 
        #print("new number is ", new_num)

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

        #print('start date and time (H:min d/m/y) = %d:%d %d/%d/%d' %(start_hour, start_minute, start_day, start_month, start_year))
        #print('end date and time (H:min d/m/y) = %d:%d %d/%d/%d' %(end_hour, end_minute, end_day, end_month, end_year))

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
        #print(pull_data_url)
        #UrlRequest(pull_data_url, on_success=partial(self.graph_function))
        global screen_height
        global screen_width
        screen_width = self.width
        screen_height = self.height

        self.brew_data_temp = UrlRequest(pull_data_url, on_success=partial(self.graph_function), on_error=partial(connection_error_popup))

    def graph_function(self, *args):
        #print("successfully read from site")
        Brew_data_str = self.brew_data_temp.result #collect result as string
        #print ("data from site:")

        temp = csv.reader(StringIO(Brew_data_str.replace('<br>', '\n ')))
        self.Brew_data_pd = pd.DataFrame(list(temp))

        new_header = self.Brew_data_pd.iloc[0]
        self.Brew_data_pd = self.Brew_data_pd[1:]
        self.Brew_data_pd.columns = new_header
        self.Brew_data_pd = self.Brew_data_pd.dropna()
        #print(self.Brew_data_pd)
        
        self.Brew_data_pd["Timestamp"] = pd.to_datetime(self.Brew_data_pd["Timestamp"], unit = 's') #convert unix to human time
        #print (self.Brew_data_pd["Timestamp"])
        
        #create the graph

        title_text = Brew_name + str(" Batch ") + batch_num

        xfmt = mpl_dates.DateFormatter('%d-%m')

        fig, ax = plt.subplots()
        ax.plot(self.Brew_data_pd["Timestamp"], self.Brew_data_pd[" Alcohol Percent"].astype('float32'))
        ax.xaxis.set_major_formatter(xfmt)
        ax.set(xlabel='Date', ylabel= self.Brew_data_pd[" Alcohol Percent"].name, title= title_text)
        ax.grid()

        self.graph = FigureCanvasKivyAgg(plt.gcf())
        self.ids.graph_display.add_widget(self.graph)

    def update_graph(self, Y_value):
        #print("entered update graph function")
        #print(self.Brew_data_pd)
        
        plt.clf() #clear the current graph

        self.ids.graph_display.remove_widget(self.graph) #clear the current graph figure
        fig, ax = plt.subplots()
        xfmt = mpl_dates.DateFormatter('%d-%m')
        ax.xaxis.set_major_formatter(xfmt)
        title_text = Brew_name + str(" Batch ") + batch_num
        ax.plot(self.Brew_data_pd["Timestamp"], self.Brew_data_pd[Y_value].astype('float32'))
        ax.set(xlabel='Date', ylabel= self.Brew_data_pd[Y_value].name, title= title_text)
        ax.grid()
        self.graph = FigureCanvasKivyAgg(plt.gcf())
        self.ids.graph_display.add_widget(self.graph)
        #FigureCanvasKivyAgg(plt.gcf())

    def reset_screen(self):
        #print("remove function")
        self.ids.graph_display.remove_widget(self.graph)

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("Alcohol by Weight.kv") #needs to be right before myMainApp 

class MyMainApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MyMainApp().run()