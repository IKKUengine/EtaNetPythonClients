import threading
import RPi.GPIO as GPIO
import parameter
import time
class OnePortGbioRpiConnection(threading.Thread):
    
    exit = True
    stop = True
    
    def __init__(self, portNumber = 24, portType = GPIO.OUT):
        threading.Thread.__init__(self)

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(portNumber, portType)
        self.portNumber = portNumber
        if parameter.printMessages:
            print("init GBIOs")
        threading.Thread.start(self)

    def run(self):
        while self.exit:
            if self.stop:
                self.request()
            time.sleep(parameter.timeTriggerConntrolling)
    
    def request(self):
        pass
    
    def setGPIOPinOnOff(self):
        GPIO.output(self.portNumber, not GPIO.input(self.portNumber))
        
    def setGPIOPinOn(self):
        GPIO.output(self.portNumber, 1)
        
    def setGPIOPinOff(self):
        GPIO.output(self.portNumber, 0)
    
    def getGPIOPinStatus(self):
        status = GPIO.input(self.portNumber)
        return status
    
    def setStop(self):
        self.stop = False

    def setStart(self):
        self.stop = True

    def setExit(self):
        self.exit = False
        