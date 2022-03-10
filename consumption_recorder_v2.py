from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.clock import Clock

#import recoder
from consumption_recorder import *

#
import json
import requests
from config_local import *


Builder.load_file('consumption_recorder_ux_definition_v2.kv')



class Hello_consumption(TabbedPanel):
    
    
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
        responseJson = json.loads(response.text)
        print(responseJson)
       
        self.myByteReceived = responseJson['bytes-received']
        self.myByteSent= responseJson['bytes-sent']
        self.myInitDate=  responseJson['init_date'].split(' ')[0]
        self.myNewsLabel=  responseJson['news_content']
        self.myEnegryConsumption = responseJson['energy_consumed_kWh']
        self.myCO2Consumption = responseJson['co2_equi_emited_kg']
        
        #self.label_data_energy_consumed= str(24)
        #self.label_data_co2_emited= str(55)
        #self.label_news= 'This is a super News1!'

        self.updateLabel()
    
    def timedAction(self, dt):
        print(str(self.projectName))
        self.myRecorder.generate_message()
        self.push_message()

    info = StringProperty()
    mycounter = 0
    myRecorder = Consumption_recorder()
    
    projectName = 'Unidentifier Project'


    #the chrono
    sendeverysecond = 300
    

    #the byte
    myByteSent = 0
    myByteReceived = 0
    myInitDate = '0000-0-0'
    myEnegryConsumption = 0
    myCO2Consumption = 0
    myNewsLabel = 'This is the news place holder!'

    #we init
    label_data_received= ObjectProperty()
    label_data_sent= ObjectProperty()
    label_data_first_date= ObjectProperty()
    label_data_energy_consumed= ObjectProperty()
    label_data_co2_emited= ObjectProperty()
    label_news= ObjectProperty()

        

    def checkbox_click(self,check,active):
        print(active)
        if active:
            #we activate
            if self.timer is not None:
                print('We activate the synchro and reset it')
                Clock.unschedule(self.timer)
            self.timer = Clock.schedule_interval(self.timedAction, self.sendeverysecond)  
        else:
            print('We activate the synchro and reset it')
            Clock.unschedule(self.timer)

    
    def forceSynchro(self):
        print('Forcing Synchro!!!!!')
        self.mycounter += 1
        self.myRecorder.generate_message() 
        self.push_message()
        self.updateLabel()
        
    
    def updateLabel(self):
        self.label_data_received.text = str(self.myByteReceived) + ' GB'
        self.label_data_sent.text = str(self.myByteSent) + ' GB'
        self.label_data_first_date.text = str(self.myInitDate)
        
        self.label_data_energy_consumed.text = str(self.myEnegryConsumption) + ' kWh'
        self.label_data_co2_emited.text = str(self.myCO2Consumption) + ' kg'
        self.label_news.text = str(self.myNewsLabel)
    
    

class TabbedPanelApp(App):
    def build(self):
        self.title = 'PALO IT Carbon Analyser'
        obj = Hello_consumption()
        obj.myRecorder.generate_message() 
        obj.push_message()
        obj.timer = Clock.schedule_interval(obj.timedAction, obj.sendeverysecond)    
        return obj


if __name__ == '__main__':
    TabbedPanelApp().run()