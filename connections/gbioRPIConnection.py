import RPi.GPIO as GPIO
import threading

class GbioRpiConnection(threading.Thread):
    
    exit = True
    stop = True
    
    def __init__(self):
        threading.Thread.__init__(self)
        #GPIO.setmode(GPIO.BOARD)
        #GPIO.setwarnings(False)
        #GPIO.setup(12, GPIO.OUT)

    #    if GPIO.input(12):
    #        self.textSignal = 'CHP is ON at Start'
    #    else:
    #        self.textSignal = 'CHP is OFF at Start'
        print("init GBIOs")
        threading.Thread.start(self)

    def run(self):
        #self.lock.acquire()
        while self.exit:#threat wird erst beendet wenn aus while schleife herausgeganen wird
            if self.stop:
                self.request()
            time.sleep(1)
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