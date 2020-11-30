from connections import gpsConnection
from observer import observe
import parameter
import datetime

class GpsModul(gpsConnection.GpsConnection, observe.Observer):

    dataStr = "0, 0, 0, 0"
    headerStr = "'Longitude [°]', 'Latitude [°]', 'Speed [m/s]', 'Altitude [m]'"

    def __init__(self, observable):
        gpsConnection.GpsConnection.__init__(self)
        observe.Observer.__init__(self, observable)

    def notifyData(self):
      return self.dataStr
    
    def notifyHeader(self):
      return self.headerStr

    def request(self):
        geo=self.getGeo()
        Lat=self.getLat(geo)
        Lon=self.getLon(geo)
        Speed=self.getSpeed(geo) #m/s
        Alt= self.getAlt(geo)
           
        self.dataStr = "{:8.4f}, {:8.4f}, {:8.1f}, {:8.1f}".format(Lon, Lat, Speed, Alt)
#         print("gpsModul: {:8.4f}, {:8.4f}, {:8.3f}, {:8.1f}".format(Lon, Lat, Speed, Alt))
    
    def getHeader(self):
        return self.headerStr
    
    def getData(self):
        return self.dataStr
                   