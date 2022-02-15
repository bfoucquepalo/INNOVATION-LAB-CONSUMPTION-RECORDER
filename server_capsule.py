#import recoder
from consumption_recorder import *

#
import json
import requests
from config_local import *

class Capsule_recorder():
    
    def __init__(self):
        self.myRecorder = Consumption_recorder()
        self.sendeverysecond = 300

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

#let's start the madness!!!!!!!!!
myCapsule = Capsule_recorder()

while 1:
    myCapsule.myRecorder.generate_message()
    myCapsule.push_message()
    time.sleep(myCapsule.sendeverysecond)
    