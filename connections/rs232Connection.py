import time
import threading
import serial
import parameter

class Rs232Connection(threading.Thread):
    
    exit = True
    stop = True

    try:     
        __ser = serial.Serial(
             port='/dev/ttyS0',  # Open RPI buit-in serial port
             baudrate=9600,
             parity=serial.PARITY_NONE,
             stopbits=serial.STOPBITS_ONE,
             bytesize=serial.EIGHTBITS,
             timeout=1
         )
    except:
        print ("RS232-Port could not be opened!")

    def __init__(self):
        threading.Thread.__init__(self)
        if parameter.printMessages:
            print("init rs232")
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
        try:
            self.__ser.close
        except:
            pass
