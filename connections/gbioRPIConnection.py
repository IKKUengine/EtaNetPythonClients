#import RPi.GPIO as GPIO
import threading

class GbioRpiConnection(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        #GPIO.setmode(GPIO.BOARD)
        #GPIO.setwarnings(False)
        #GPIO.setup(12, GPIO.OUT)

    #    if GPIO.input(12):
    #        self.textSignal = 'CHP is ON at Start'
    #    else:
    #        self.textSignal = 'CHP is OFF at Start'
        pass

    def run(self):
        #self.lock.acquire()
        self.request()
        #self.lock.release()

    def request(self):
        pass

    def __exit__(self):
        #GPIO.cleanup()
        pass