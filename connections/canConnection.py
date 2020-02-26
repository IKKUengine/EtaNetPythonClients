import time
import threading
import can
import parameter

class CANConnection(threading.Thread):
    
    exit = True
    stop = True
    
# sudo /sbin/ip link set can0 up type can bitrate 500000 #Code for connection to PiCAN2 via terminal
# bus = can.interface.Bus(channel='can0', bustype='socketcan_native')#, bitrate=500000)

    def __init__(self):
        self.ser = can.interface.Bus(channel='can0', bustype='socketcan_native')
        self.SoC_message = can.Message(arbitration_id=0x6F1,data=[0x07, 0x03, 0x22, 0xDD, 0xC4, 0x00, 0x00, 0x00],extended_id=False)
#         self.SoH_message = can.Message(arbitration_id=0x6F1,data=[0x07, 0x03, 0x22, 0xDD, 0x7B, 0x00, 0x00, 0x00],extended_id=False)

        threading.Thread.__init__(self)
        if parameter.printMessages:
            print("init CAN")
        threading.Thread.start(self)

    def run(self):
        #self.lock.acquire()
        while self.exit:#threat wird erst beendet wenn aus while schleife herausgeganen wird
            if self.stop:
                self.request()
            time.sleep(parameter.timeTriggerECar)
            #self.lock.release()

    def request(self):
        pass

    def getCanPort(self):
        return self.ser
    
    
    def getMessageSoC(self):
        return self.SoC_message
    
#     def getMessageSoH(self):
#         return self.SoH_message
       

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
