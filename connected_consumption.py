#Kivy Import
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.textinput import TextInput

#import recoder
from consumption_recorder import *

#
import json
import requests
from config_local import *


#class Storage_Consumption_data():#
#

class Hello_consumption(App):
    

    def build(self):
        #
        self.myRecorder = Consumption_recorder()
        textinput = TextInput(text='Unidentifier Project')
        textinput.bind(text=self.on_text)
        self.timer = None
        self.projectName = textinput.text
        
        #the layout
        superBox = BoxLayout(orientation='vertical')
        horizontalBox1   = BoxLayout(orientation='horizontal')
        btn1 = Button(text='Click to start to push Data')
        btn1.bind(state=self.callbackStart)
        btn2 = Button(text='Click to stop to push Data')
        btn2.bind(state=self.callbackStop)
        labelHeader = Label(text='Your identifier is: ' + str(self.myRecorder.myHeader) + '\n\n\nChange your project name below')

        #bl = BoxLayout()
        horizontalBox1.add_widget(btn1)
        horizontalBox1.add_widget(btn2)
        superBox.add_widget(labelHeader)
        
        superBox.add_widget(textinput)
        superBox.add_widget(horizontalBox1)
        #
        # we init
        self.myRecorder.generate_message() 
        self.push_message()
        return superBox

    def on_text(self,instance, value):
        print('The widget', instance, 'have:', value)
        self.projectName = str(value)
        self.myRecorder.myHeader['project'] = str(value)


    def callbackStart(self, instance, value):
        print('My button1 <%s> state is <%s>' % (instance, value))
        if self.timer is not None:
            Clock.unschedule(self.timer)
        self.timer = Clock.schedule_interval(self.timedAction, 10)        

    def callbackStop(self, instance, value):
        print('My button2 <%s> state is <%s>' % (instance, value))
        Clock.unschedule(self.timer)

    def timedAction(self, dt):
        print(str(self.projectName))
        self.myRecorder.generate_message()
        self.push_message()
    
    def push_message(self):
        print(self.myRecorder.myMessage)
        
        API_END_POINT_SERVICE = 'dev/get_consumption_data'

        PostAddressGetInfoElement = API_ENDPOINT_ROOT + '/' + API_END_POINT_SERVICE
        token = 'no_token'
        PostData={}
        PostData['message']=self.myRecorder.myMessage


        response = requests.post(PostAddressGetInfoElement,data=json.dumps(PostData),headers = {"Content-Type":"application/json","Authorization":"Bearer " + token,"x-api-key":API_KEY})

        print('POST STATUS: ' + str(response.status_code) + ' REASON: ' +  str(response.reason))

        print('POST ANSWER: ' + response.text)

if __name__ == '__main__':
    Hello_consumption().run()