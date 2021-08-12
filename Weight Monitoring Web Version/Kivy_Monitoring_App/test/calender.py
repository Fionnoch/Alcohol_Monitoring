import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty

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

class DateTimeSelector(Widget): #create the widget
    input_start_day = ObjectProperty(None)
    input_start_month = ObjectProperty(None)
    input_start_year = ObjectProperty(None)
    input_start_minute = ObjectProperty(None)
    input_start_hour = ObjectProperty(None)

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

class DateTestApp(App): #creates the app
    def build(self):
        return DateTimeSelector()

if __name__ == '__main__': #runs the app 
    DateTestApp().run()
 