import time
import threading
import gps
import parameter
import socket 
import serial
from ublox_gps import UbloxGps

class GpsConnection(threading.Thread):
    
    exit = True
    stop = True

    def __init__(self):
        
        try:
            self.port = serial.Serial('/dev/gps0', baudrate=38400, timeout=1)
            self.gps = UbloxGps(self.port)
            threading.Thread.__init__(self)        
            threading.Thread.start(self)
            print("socket is created")
        except:            
            print("socket NOT created")

    def run(self):
        while self.exit:#threat wird erst beendet wenn aus while schleife herausgeganen wird
            if self.stop:
                self.request()
            time.sleep(parameter.timeTriggerGps)
    
    def request(self):
        pass

    def setStop(self):
        self.stop = False

    def setStart(self):
        self.stop = True

    def setExit(self):
        self.exit = False

    def getGeo(self):
        geo = self.gps.geo_coords()
        return geo

    # get Latitude
    def getLat(self, geo):
            lat=geo.lat
            return lat

    # get Longitude
    def getLon(self, geo):
            lon=geo.lon
            return lon
    
    # get Speed
    def getSpeed(self, geo):
            speed=geo.gSpeed*0.001 #m/s
            return speed
        
    # get Altitude
    def getAlt(self, geo):
            alt=geo.hMSL/1000 #m
            return alt


