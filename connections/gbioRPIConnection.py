import threading
import RPi.GPIO as GPIO
import parameter
import time
class GbioRpiConnection(threading.Thread):
    
    exit = True
    stop = True
    
    def __init__(self, portNumber = 12, portType = GPIO.OUT):
        threading.Thread.__init__(self)

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(portNumber, portType)
        self.portNumber = portNumber
        if parameter.printMessages:
            print("init GBIOs")
        threading.Thread.start(self)

    def run(self):
        while self.exit:#threat wird erst beendet wenn aus while schleife herausgeganen wird
            if self.stop:
                self.request()
            time.sleep(parameter.timeTriggerConntrolling)
    
    def request(self):
        pass
    
    def setRelaisCHPOnOff(self):
        #if GPIO.input(12):
            #self.signalText['text'] = 'CHP is OFF'
        #else:
            #self.signalText['text'] = 'CHP is ON'
        GPIO.output(self.portNumber, not GPIO.input(self.portNumber))
    
    def getCHPOnOffStatus(self):
        status = GPIO.input(self.portNumber)
        return status
    
    def setStop(self):
        self.stop = False

    def setStart(self):
        self.stop = True

    def setExit(self):
        self.exit = False
        