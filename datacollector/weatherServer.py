import parameter
import json, requests
from connections import internetConnection
from connections import gpsConnection
from observer import observe
import datetime

import time

class Weather(internetConnection.WeatherServer, gpsConnection.GpsConnection, observe.Observer):
    
    dataStr = "0, 0, 0"
    headerStr = "'Outside Temp. [°C]', 'Pressure [Pa]','WeatherDescription [ ]'"
    
    def __init__(self, observable):
        internetConnection.WeatherServer.__init__(self)
        gpsConnection.GpsConnection.__init__(self)
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
#             print("Weather Server: {:8.2f}, {:8.2f}, {}".format(Tout, Pout,weatherDesc) )
        except:
            print("Weather did not get data")
    
    def getHeader(self):
        return self.header
    
    def getData(self):
        return self.data
