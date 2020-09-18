import time
import threading
import gps
import parameter

class GpsConnection(threading.Thread):
    
    exit = True
    stop = True

    def __init__(self):

        threading.Thread.__init__(self)

        #Please set your gps connection init code
        
        if parameter.printMessages:
            print("init gps")
        threading.Thread.start(self)

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


