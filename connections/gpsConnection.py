import time
import threading
import gps
import parameter
import socket #added

class GpsConnection(threading.Thread):
    
    exit = True
    stop = True

    def __init__(self):
        
        try:
            # Listen on port 2947 (gpsd) of localhost
            self.session = gps.gps("localhost", "2947")
            self.session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
            threading.Thread.__init__(self)        
            threading.Thread.start(self)

            #if parameter.printMessages:
            print("socket is created")
            
        except:            
            print("socket NOT created")

    def run(self):
        #self.lock.acquire()
        while self.exit:#threat wird erst beendet wenn aus while schleife herausgeganen wird
            if self.stop:
                self.request()
            time.sleep(parameter.timeTriggerGps)
            #self.lock.release()
    
    def request(self):
        pass

    def setStop(self):
        self.stop = False

    def setStart(self):
        self.stop = True

    def setExit(self):
        self.exit = False

    #GPS Sensor Functions
    def getReport(self):
        report = self.session.next()
        return report

    def getLat(self, report):
        if report['class'] == 'TPV':
            lat=report.lat
            return lat

    def getLon(self, report):
        if report['class'] == 'TPV':
            lon=report.lon
            return lon
    
    def getSpeed(self, report):
        if report['class'] == 'TPV':
            speed=report.speed
            return speed

