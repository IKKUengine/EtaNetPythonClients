from observer import observe
from connections import fileConnection
import parameter
import datetime

class TemperatureSensor(fileConnection.FileConnection, observe.Observer):

    dataStr = "'NaN'"
    headerStr = "'Inside Temp. [°C]'"

    def __init__(self, observable):
       # rs232Connection.Rs232Connection.__init__()
        #observe.Observer.__init__(observable)
        fileConnection.FileConnection.__init__(self)
        observe.Observer.__init__(self, observable)
        
        
    def notifyData(self):
      return self.dataStr
    
    def notifyHeader(self):
      return self.headerStr

    def request(self):
        
        try:
            # read data of file
            #temperatureInside
            
            #self.dataStr = "{:8.6f},".format(temperatureInside)
            print ("Temperature sensor is switched on!")
        except:
            pass
            
    def getHeader(self):
        return self.headerStr
    
    def getData(self):
        return self.dataStr