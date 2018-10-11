import threading
import RPi.GPIO as GPIO
import error
class GbioRpiConnection(threading.Thread):
    
    exit = True
    stop = True
    
    def __init__(self, portNumber = 12, portType = GPIO.OUT):
        threading.Thread.__init__(self)
        threading.Thread.start(self)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(portNumber, portType)
        if error.printMessages:
            print("init GBIOs")

    def run(self):
        self.request()

    def setRelais(self):
        #if GPIO.input(12):
            #self.signalText['text'] = 'CHP is OFF'
        #else:
            #self.signalText['text'] = 'CHP is ON'
        GPIO.output(12, not GPIO.input(12))
    
    def request(self):
        pass
    