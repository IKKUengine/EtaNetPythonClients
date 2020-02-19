import threading
import RPi.GPIO as GPIO
import parameter
import time
class OnePortGbioRpiConnection(threading.Thread):
    
    exit = True
    stop = True
    
    def __init__(self, portNumber1 = 24, portType1 = GPIO.OUT, portNumber2 = 23, portType2 = GPIO.IN):
        threading.Thread.__init__(self)

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(portNumber1, portType1)
        GPIO.setup(portNumber2, portType2)
        self.portNumber1 = portNumber1
        self.portNumber2 = portNumber2
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
        GPIO.output(self.portNumber1, not GPIO.input(self.portNumber1))
        
    def setGPIOPinOn(self):
        GPIO.output(self.portNumber1, 1)
        
    def setGPIOPinOff(self):
        GPIO.output(self.portNumber1, 0)
    
    def getGPIOPinStatus1(self):
        status = GPIO.input(self.portNumber1)
        return status
        
    def getGPIOPinStatus2(self):
        status = GPIO.input(self.portNumber2)
        return status
    
    def setStop(self):
        self.stop = False

    def setStart(self):
        self.stop = True

    def setExit(self):
        self.exit = False
        