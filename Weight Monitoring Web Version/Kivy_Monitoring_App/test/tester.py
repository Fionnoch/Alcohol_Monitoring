from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder


Builder.load_string('''
<MyWidget>:
    Button:
        id: id_value_1
        text: 'Print my id'
        on_press: print({'id_value_1': self.proxy_ref})
    Button:
        id: id_value_2
        text: 'Print all ids'
        on_press: print(root.ids)
''')


class MyWidget(BoxLayout):
    pass


class MyApp(App):
    def build(self):
        widget = MyWidget()
        print({'id_value_1': widget.ids['id_value_1']})
        return widget


if __name__ == '__main__':
    MyApp().run()