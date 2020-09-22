import parameter
import json, requests
from connections import internetConnection
from observer import observe
import datetime

import time

class Weather(internetConnection.WeatherServer, observe.Observer):
    
    
    dataStr = "0, 0, 0"
    headerStr = "'Outside Temp. [°C]', 'Pressure [Pa]','WeatherDescription [ ]'"
    
    
    def __init__(self, observable):
        internetConnection.WeatherServer.__init__(self)
        observe.Observer.__init__(self, observable)


    def notifyData(self):
      return self.dataStr
    
    def notifyHeader(self):
      return self.headerStr

    def request(self):
        try:
            #set workflow for data reading
            weather=self.getAPI()
            #tempuratureOut
            Tout = self.getTempOut(weather)
            #pressureOut
            Pout = self.getPressure(weather)
            #weatherDescription
            weatherDesc = self.getWeather(weather)

            print ("Weather server connection is done!")
            self.dataStr = "{:8.2f}, {:8.2f}, {}".format(Tout, Pout,weatherDesc)       
        except:
            print("Weather did not get data")
    
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
        