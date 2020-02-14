import time
import threading
import serial
import parameter

class CANConnection(threading.Thread):
    
    exit = True
    stop = True
    
# sudo /sbin/ip link set can0 up type can bitrate 500000 #Code for connection to PiCAN2 via terminal
# bus = can.interface.Bus(channel='can0', bustype='socketcan_native')#, bitrate=500000)

    try:     
        __ser = can.interface.Bus(channel='can0', bustype='socketcan_native')
    except:
        print ("CAN-Port could not be opened!")

    def __init__(self):
        threading.Thread.__init__(self)
        if parameter.printMessages:
            print("init CAN")
        threading.Thread.start(self)

    def run(self):
        #self.lock.acquire()
        while self.exit:#threat wird erst beendet wenn aus while schleife herausgeganen wird
            if self.stop:
                self.request()
            time.sleep(parameter.ECar)
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
