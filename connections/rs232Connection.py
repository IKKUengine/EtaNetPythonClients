import time
import threading
import serial

class Rs232Connection(threading.Thread):
    
    exit = True
    stop = True

    __ser = serial.Serial(
         port='/dev/ttyS0',  # Open RPI buit-in serial port
         baudrate=9600,
         parity=serial.PARITY_NONE,
         stopbits=serial.STOPBITS_ONE,
         bytesize=serial.EIGHTBITS,
         timeout=1
     )

    def __init__(self):
        threading.Thread.__init__(self)
        print("init rs232")
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


