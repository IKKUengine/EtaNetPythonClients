import time
import threading
import parameter
import glob

class FileConnection(threading.Thread):
    
    exit = True
    stop = True


    def __init__(self):
        threading.Thread.__init__(self)
        
        #base_dir = '/sys/bus/w1/devices/'
        #while True:
        #    try:
        #        self.device_folder = glob.glob(base_dir + '28*')[0]
        #        break
        #    except IndexError:
        #        sleep(0.5)
        #        continue
        #self.device_file = self.device_folder + '/w1_slave'

        # To initialise, the sensor will be read "blind"
        #read_temp_raw(self.device_file)
        
        
        if parameter.printMessages:
            print("init file connection")
        threading.Thread.start(self)

    def run(self):
        #self.lock.acquire()
        while self.exit:#threat wird erst beendet wenn aus while schleife herausgeganen wird
            if self.stop:
                self.request()
            time.sleep(parameter.timeTriggerPowerAnalayser)
            #self.lock.release()

    def request(self):
        pass

    def getSerialPort(self):
        return self.__ser

    def setStop(self):
        self.stop = False

    def setStart(self):
        self.stop = True

    def setExit(self):
        self.exit = False
        
    def __exit__(self):
        pass