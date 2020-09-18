import parameter
import json, requests
from connections import internetConnection
from observer import observe
import datetime

import time

class Weather(internetConnection.WeatherServer, observe.Observer):
    
    
    dataStr = "'NaN', 'NaN'"
    headerStr = "'Outside Temp. [°C]', 'Pressure [Pa]'"
    
    
    def __init__(self, observable):
        internetConnection.WeatherServer.__init__(self)
        observe.Observer.__init__(self, observable)


    def notifyData(self):
      return self.dataStr
    
    def notifyHeader(self):
      return self.headerStr

    def request(self):
        print ("Weather server connection is done!")
        try:
            pass
            #set workflow for data reading 
            #tempuratureOut
            #pressureOut
            
            #self.dataStr = "{:8.6f}, {:8.6f}".format(tempuratureOut, pressureOut)       
        except:
            pass
        
    # set funktion here, do not forget the self
    def getTreturn(self):
        return self.returnT

    def getHeader1(self):
        return self.headerH1

    def getHeader2(self):
        return self.headerH2
    
    def getHeader3(self):
        return self.headerH3
    
    def getData1(self):
        return self.data1
    def getData2(self):
        return self.data2
    def getData3(self):
        return self.data3
        