import time
import threading
import parameter
import datetime

from observer import observe

class WeatherServer(threading.Thread):
    exit = True
    stop = True
    
    def __init__(self):

        try:                       
            threading.Thread.__init__(self)
            threading.Thread.start(self)
            
        except:          
            print("Weather thread can not start!")

    def run(self):  
        while self.exit:
            if self.stop:
                self.request()
            time.sleep(parameter.timeTriggerMeterbus)
                
    def request(self):
        pass
     
        
    # set function here, do not forget the self
    
    def setStop(self):
        self.stop = False

    def setStart(self):
        self.stop = True

    def setExit(self):
        self.exit = False

    def __exit__(self):
        pass
        
        
class CloudConnection(threading.Thread, observe.Observable):
    
    exit = True
    stop = True
    messageServer = "NO CLOUD CONNECTION!"
    feedback = "Ready to get feedback!"
    
    def __init__(self):

        observe.Observable.__init__(self)
        threading.Thread.__init__(self)

        threading.Thread.start(self)
        
    def run(self):
        while self.exit:
            if self.stop:
                self.notify_observersMonitoring()
                time.sleep(parameter.timeTriggerSendData)
                self.sendAllData()
       
    def setIP(self, host):
        self.host = host
        
    def getIP(self):
        return "123456"    
    
    def sendAllData(self):

        datetimeCloud = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message =  "'{}' ('TimeStamp', {}) VALUES ('{}', {})".format(parameter.systemIdentifier, self.getHeaderList(), datetimeCloud , self.getDataList()) 
            
        try:
            #inside "message" you have all information about weather gps and tem sensor
            # it a string
            print (message)
            self.messageServer = "WITH IoT-CLOUD CONNECTED!"
            #print("SERVER CONNECTED!")
        except:
            if parameter.printMessages:
                print ("Please switch mount USB-Internetstick!")
            self.messageServer = "NO CLOUD CONNECTED!"

     
    # set your fkt here! do not forget self
    def setStop(self):
        self.stop = False

    def setStart(self):
        self.stop = True

    def setExit(self):
        self.exit = False
    
    def getMessageServer(self):
        return self.messageServer
    
    def getFeedback(self):
        return self.feedback
    

    def __exit__(self):
        self.messageServer = "NO SERVER CONNECTED!"