import kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.textinput import TextInput


#class Storage_Consumption_data():#
#

class Hello_consumption(App):
    

    def build(self):
        textinput = TextInput(text='Hello world')
        textinput.bind(text=self.on_text)
        self.timer = None
        self.projectName = textinput.text

        #the layout
        superBox = BoxLayout(orientation='vertical')
        horizontalBox1   = BoxLayout(orientation='horizontal')
        btn1 = Button(text='Click to start')
        btn1.bind(state=self.callbackStart)
        btn2 = Button(text='Click to stop')
        btn2.bind(state=self.callbackStop)
        labelHeader = Label(text='Hello world')

        #bl = BoxLayout()
        horizontalBox1.add_widget(btn1)
        horizontalBox1.add_widget(btn2)
        superBox.add_widget(labelHeader)
        
        superBox.add_widget(textinput)
        superBox.add_widget(horizontalBox1)
        return superBox

    def on_text(self,instance, value):
        print('The widget', instance, 'have:', value)
        self.projectName = str(value)


    def callbackStart(self, instance, value):
        print('My button1 <%s> state is <%s>' % (instance, value))
        if self.timer is not None:
            Clock.unschedule(self.timer)
        self.timer = Clock.schedule_interval(self.timedAction, 0.5)        

    def callbackStop(self, instance, value):
        print('My button2 <%s> state is <%s>' % (instance, value))
        Clock.unschedule(self.timer)

    def timedAction(self, dt):
        print(str(self.projectName))

if __name__ == '__main__':
    Hello_consumption().run()