
from connections import gpsConnection
from observer import observe
import parameter
import datetime

class GpsModul(gpsConnection.GpsConnection, observe.Observer):

    dataStr = "'NaN', 'NaN', 'NaN'"
    headerStr = "'Longitude [°]', 'Latitude [°]', 'Speed [km/h]'"

    def __init__(self, observable):
       # rs232Connection.Rs232Connection.__init__()
        #observe.Observer.__init__(observable)
        gpsConnection.GpsConnection.__init__(self)
        observe.Observer.__init__(self, observable)

    def notifyData(self):
      return self.dataStr
    
    def notifyHeader(self):
      return self.headerStr

    def request(self):
        try:
            pass
            #Please set here your gps data request code
            #longitude
            #latitude
            #speed (m/s -> km/h)

        except:
            print ("GPS Sensor is switched off!")
        try:
            pass
            #self.dataStr = "{:8.6f}, {:8.6f}, {:8.6f}".format(longitude, latitude, speed)       
        except:
            pass
        
    def getHeader(self):
        return self.headerStr
    
    def getData(self):
        return self.dataStr
                   