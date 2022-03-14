from copy import deepcopy
import psutil
import copy
import time
import hashlib
import uuid
import datetime

class Consumption_recorder():
    
    def __init__(self):
        #we generate the run_UUID
        self.myRunUUID = str(uuid.uuid4())

        #Network
        self.myNetworkDico ={}
        self.myNetworkDicoHistory ={}
        self.counterSentmyNetwork = 0
        #process
        self.myProcessDico ={}
        self.myProcessDicoHistory ={}
        self.counterProcess = 0
        #message
        self.myMessage = {}
        self.userList = []
        #cpu
        self.counterCPU = 0
        self.myCPUDico = {}
        self.myCPUDico['user'] = 0
        self.myCPUDico['nice'] = 0
        self.myCPUDico['system'] = 0
        self.myCPUDico['idle'] = 0
        #cpu total
        self.myCPUDico['user_total'] = 0
        self.myCPUDico['nice_total'] = 0
        self.myCPUDico['system_total'] = 0
        self.myCPUDico['idle_total'] = 0
        #header
        self.myHeader = {}
        self.myHeader['project']='init project'
        #time active
        self.myHeader['active_duration_s'] = 0
        self.myActiveTimeS = 0
        self.lastDatePush = datetime.datetime.now()


        #we get the user list
        for userInfo in psutil.users():
            if str(hashlib.md5(userInfo.name.encode('utf-8')).hexdigest()) not in self.userList:
                #userList.append(str(hashlib.md5(userInfo.name.encode('utf-8')).hexdigest()))
                self.myHeader['user_list']=[]
                currentUser={}
                currentUser['user_hashed'] = str(hashlib.md5(userInfo.name.encode('utf-8')).hexdigest())
                currentUser['run_uuid'] =self.myRunUUID
                #self.myHeader[str(hashlib.md5(userInfo.name.encode('utf-8')).hexdigest())] = self.myRunUUID
                self.myHeader['user_list'].append(currentUser)

        #print(self.myHeader)

    def generate_message(self,stepDuration_S):
        print('start generating message')
        self.myMessage={}
        self.myMessage['header'] = self.myHeader
        #duration
        self.myMessage['header']['duration'] = stepDuration_S
        self.lastDatePush = datetime.datetime.now()
        #print(psutil.cpu_times())
        myCPU = psutil.cpu_times()
        
        self.counterCPU += 1
        self.myCPUDico['run_uuid']=self.myRunUUID
        self.myCPUDico['sequence_cpu']=str(self.counterCPU)
        if self.counterCPU ==1:
            self.myCPUDico['user'] = 0
            self.myCPUDico['nice'] = 0
            self.myCPUDico['system'] = 0
            self.myCPUDico['idle'] = 0
            #total
            self.myCPUDico['user_total'] = myCPU.user
            self.myCPUDico['nice_total'] = myCPU.nice
            self.myCPUDico['system_total'] = myCPU.system
            self.myCPUDico['idle_total'] = myCPU.idle
        else:
            self.myCPUDico['user'] = myCPU.user - self.myCPUDico['user_total']
            self.myCPUDico['nice'] = myCPU.nice - self.myCPUDico['nice_total']
            self.myCPUDico['system'] = myCPU.system - self.myCPUDico['system_total']
            self.myCPUDico['idle'] = myCPU.idle - self.myCPUDico['idle_total']
            #total
            self.myCPUDico['user_total'] = myCPU.user
            self.myCPUDico['nice_total'] = myCPU.nice
            self.myCPUDico['system_total'] = myCPU.system
            self.myCPUDico['idle_total'] = myCPU.idle
        
        #print(self.myCPUDico)
        #
        self.myMessage['info_cpu'] = self.myCPUDico
        
        myNetwork = psutil.net_io_counters(pernic=True)
        self.counterSentmyNetwork += 1
        for net in myNetwork:
            #print(myNetwork[net].bytes_sent)
            #snetio(bytes_sent=127124480, bytes_recv=127124480
            currentInterfaceName = str(net)
            bytes_sent = 0
            bytes_recv= 0
            self.myNetworkDico[currentInterfaceName]={}
            self.myNetworkDico[currentInterfaceName]['run_uuid']=self.myRunUUID
            self.myNetworkDico[currentInterfaceName]['sequence_network']=str(self.counterSentmyNetwork)
            self.myNetworkDico[currentInterfaceName]['network_line_uuid']=str(uuid.uuid4())
            
            if net in self.myNetworkDicoHistory:
                self.myNetworkDico[currentInterfaceName]['network_name'] = str(currentInterfaceName)
                bytes_sent = myNetwork[currentInterfaceName].bytes_sent
                bytes_sent_old = self.myNetworkDicoHistory[currentInterfaceName]['bytes_sent']
                self.myNetworkDico[currentInterfaceName]['bytes_sent'] = round(myNetwork[currentInterfaceName].bytes_sent - self.myNetworkDicoHistory[currentInterfaceName]['bytes_sent_total'],3)
                self.myNetworkDico[currentInterfaceName]['bytes_recv'] = round(myNetwork[currentInterfaceName].bytes_recv - self.myNetworkDicoHistory[currentInterfaceName]['bytes_recv_total'],3)
                #total
                self.myNetworkDico[currentInterfaceName]['bytes_sent_total'] = round(myNetwork[currentInterfaceName].bytes_sent,3)
                self.myNetworkDico[currentInterfaceName]['bytes_recv_total'] = round(myNetwork[currentInterfaceName].bytes_recv,3)
            else:
                self.myNetworkDico[currentInterfaceName]['network_name'] = str(currentInterfaceName)
                bytes_sent = myNetwork[currentInterfaceName].bytes_sent
                self.myNetworkDico[currentInterfaceName]['bytes_sent'] = 0
                self.myNetworkDico[currentInterfaceName]['bytes_recv'] = 0
                #total
                self.myNetworkDico[currentInterfaceName]['bytes_sent_total'] = round(myNetwork[currentInterfaceName].bytes_sent,3)
                self.myNetworkDico[currentInterfaceName]['bytes_recv_total'] = round(myNetwork[currentInterfaceName].bytes_recv,3)

        self.myNetworkDicoHistory = copy.deepcopy(self.myNetworkDico)
        self.myNetworkDico = {}
        #print(myNetworkDicoHistory)
        self.myMessage['info_network'] = self.myNetworkDicoHistory
        
        # Network
        self.counterProcess += 1 
        myProcessIdList = psutil.pids()
        for currProcessId in myProcessIdList:
            currentProcessKey = ''
            currentProcessName = ''
            currentProcessCPUInfo = ''
            userTime = 0
            systemTime = 0
            try:
                currProcess = psutil.Process(currProcessId)
                currentProcessName= str(currProcess.name())
                currentProcessKey = currentProcessName + '_'+ str(currProcessId)
                currentProcessCPUInfo = currProcess.cpu_times()
                self.myProcessDico[currentProcessKey]={}
                self.myProcessDico[currentProcessKey]['run_uuid']=self.myRunUUID
                self.myProcessDico[currentProcessKey]['process_line_uuid']=str(uuid.uuid4())
                self.myProcessDico[currentProcessKey]['sequence_process']=str(self.counterProcess)

                if currentProcessKey in self.myProcessDicoHistory:
                    self.myProcessDico[currentProcessKey]['process_name'] =currentProcessName
                    self.myProcessDico[currentProcessKey]['user_time'] = round(currentProcessCPUInfo.user - self.myProcessDicoHistory[currentProcessKey]['user_time_total'],3)
                    self.myProcessDico[currentProcessKey]['system_time'] = round(currentProcessCPUInfo.system - self.myProcessDicoHistory[currentProcessKey]['system_time_total'],3)
                    #total
                    self.myProcessDico[currentProcessKey]['user_time_total'] = round(currentProcessCPUInfo.user,3)
                    self.myProcessDico[currentProcessKey]['system_time_total'] = round(currentProcessCPUInfo.system,3)
                else:
                    self.myProcessDico[currentProcessKey]['process_name'] =currentProcessName
                    self.myProcessDico[currentProcessKey]['user_time'] = 0
                    self.myProcessDico[currentProcessKey]['system_time'] = 0
                    #total
                    self.myProcessDico[currentProcessKey]['user_time_total'] = round(currentProcessCPUInfo.user,3)
                    self.myProcessDico[currentProcessKey]['system_time_total'] = round(currentProcessCPUInfo.system,3)
            except Exception as e:
                a = 12
            finally:
                a = 12

        self.myProcessDicoHistory = copy.deepcopy(self.myProcessDico)
        self.myProcessDico ={}
        #print(self.myProcessDicoHistory)
        self.myMessage['info_process'] = self.myProcessDicoHistory

        
        #the end
        #time.sleep(1)
        #print('----------------------------------------------' + str(counterCPU))
        #print('----------------------------------------------' + str(self.counterProcess))
        #print('----------------------------------------------' + str(self.counterSentmyNetwork))
        #
        return 0
