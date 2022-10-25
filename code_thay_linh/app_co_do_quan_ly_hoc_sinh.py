from turtle import width
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class MyGridLayout(GridLayout):
    # Initialized infinite keyboard
    def __init__(self, **kwargs):
        #call grid layout constructor
        super(MyGridLayout, self).__init__(**kwargs)

        #Set columns
        self.cols = 1

        #create a second grid layout
        self.top_grid = GridLayout()
        self.top_grid.cols = 2



        #Add widgets
        # self.add_widget(Label(text='Name: '))
        self.top_grid.add_widget(Label(text='Name: '))


        #Add Input Box
        # self.name = TextInput(multiline=False)
        self.name = TextInput(multiline=True)

        # self.add_widget(self.name)
        self.top_grid.add_widget(self.name)


        #Add widgets
        # self.add_widget(Label(text='Favorite Pizza: '))
        self.top_grid.add_widget(Label(text='Favorite Pizza: '))

        #Add Input Box
        self.pizza = TextInput(multiline=False)
        # self.add_widget(self.pizza)
        self.top_grid.add_widget(self.pizza)


        #Add widgets
        # self.add_widget(Label(text='Favorite Color: '))
        self.top_grid.add_widget(Label(text='Favorite Color: '))


        #Add Input Box
        self.color = TextInput(multiline=False)
        # self.add_widget(self.color)
        self.top_grid.add_widget(self.color)

        #Add the new top grid to our app
        self.add_widget(self.top_grid)



        #Create a submit Button
        self.submit = Button(text = 'Submit',
            font_size = 32,
            size_hint_y = None,
            height = 50,
            size_hint_x = None,
            width = 200
            )
        # self.add_widget(self.submit)
        
        #Bind the button
        self.submit.bind(on_press = self.press)
        self.add_widget(self.submit)

    def press(self, instance):
        name = self.name.text
        pizza = self.pizza.text
        color = self.color.text

        print(f'hello {name}, you like {pizza} pizza and your favorite color is {color}')

        #Print it to the screen
        self.add_widget(Label(text=f'hello {name}, you like {pizza} pizza and your favorite color is {color}'))

        #clear the input boxes
        self.name.text = ''
        self.pizza.text = ''
        self.color.text = ''


class MyApp(App):
    def build(self):
        # return Label(text="Hello world", font_size = 72)
        return MyGridLayout()

if __name__ == "__main__":
    MyApp().run()

