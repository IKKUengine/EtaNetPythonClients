
from connections import gpsConnection
from observer import observe
import parameter
import datetime

class GpsModul(gpsConnection.GpsConnection, observe.Observer):

    dataStr = "0, 0, 0"
    headerStr = "'Longitude [°]', 'Latitude [°]', 'Speed [km/h]'"
    Longitude =[]
    Latitude = [] 

    def __init__(self, observable):
        gpsConnection.GpsConnection.__init__(self)
        observe.Observer.__init__(self, observable)

    def notifyData(self):
      return self.dataStr
    
    def notifyHeader(self):
      return self.headerStr

    def request(self):
        #try:
        #Longitude =[]
        #Latitude = [] 
        report = self.getReport()
        Lat=self.getLat(report)
        Lon=self.getLon(report)
        Speed=self.getSpeed(report)
        #print(Lat)
        #print(Speed)
        
        #if report['class'] == 'TPV':
        #    print(">>>>>>GPS Data is shown")
        #    #longitude
        #    lon=report.lon
        #    #latitude
        #    lat=report.lat
        #    #speed (m/s -> km/h)
        #    speed= ((report.speed)*3600)/1000
        if (Lat is not None) and (Lon is not None):

            if (self.Latitude == []) and (self.Longitude == []):
                self.Longitude.append(Lon)
                self.Latitude.append(Lat)
                self.dataStr = "{:8.6f}, {:8.6f}, {:8.6f}".format(self.Longitude[0], self.Latitude[0], Speed)
                pass
            else :
                self.Longitude.append(Lon)
                self.Latitude.append(Lat)
        #print('GPS Location : %.5f°N, %.5f°E' %(self.Longitude[-1],self.Latitude[-1]))
           
                self.dataStr = "{:8.4f}, {:8.4f}, {:8.3f}".format(self.Longitude[-1], self.Latitude[-1], Speed)
    
        #except:
         #   print('gps not connected')
            

    def getHeader(self):
        return self.headerStr
    
    def getData(self):
        return self.dataStr
                   