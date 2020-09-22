from observer import observe
from connections import fileConnection
import parameter
import datetime

class TemperatureSensor(fileConnection.FileConnection, observe.Observer):

    dataStr = "0"
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
            print("Temp sensor on")
            # read data of file
            #temperatureInside
            # To initialise, the sensor will be read "blind"
            lines = self.read_temp_raw()
#              print(lines)
            TempIn = self.read_temp(lines)
#             print('Indoor Temperature : ', TempIn, '°C')
            
            self.dataStr = "{:8.2f}".format(TempIn)
            print ("Temperature sensor is switched on!")
        except:
#             print("temp did not read")
            pass
            
    def getHeader(self):
        return self.headerStr
    
    def getData(self):
        return self.dataStr
    
    
