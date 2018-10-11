import time
import threading
import socket
import error

from observer import observe

class MBusConnection(threading.Thread, observe.Observable):
    exit = True
    stop = True
    

    def __init__(self, host = '192.168.178.66', port = 10001, primeAdress = 1):

        self.host = host
        self.port = port
        self.addr = primeAdress
        if error.printMessages:
            print ('init MBus Connection')
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:        
            self.s.connect((self.host, self.port))
            if error.printMessages:
                print('Connection Mbus is done')
            self.initDevice(primeAdress)
        except:
            print ('Connection Mbus cound not done!!!')
        threading.Thread.__init__(self)
        observe.Observable.__init__(self)
        threading.Thread.start(self)

    def run(self):
   
        while self.exit:#threat wird erst beendet wenn aus while schleife herausgeganen wird
            if self.stop:
                self.request()
            time.sleep(1)
            
    
    def initDevice(self, primeAdress):
        #self.s.send("\x10\x40\x01\x41\x16".encode())
        self.s.send(self.getInitDeviceCode(self.addr).encode())
        if error.printMessages:
            print('Mbus init data are sent')
        respond = self.s.recv(1)
        if respond == b'\xe5':
            if error.printMessages:
                print('Mbus init war erfolgreich!!!')
        else:
            print('MBus init NICHT erfolgreich!!!')

    def getInitDeviceCode(self, primeAdress):
        cs = 64 + primeAdress
        RequestShortFrame = "\x10\x40{}{}\x16".format(chr(primeAdress), chr(cs))
        return RequestShortFrame
    
    def getDataDeviceCode(self, primeAdress):
        cs = 123 + primeAdress
        RequestShortFrame = "\x10{}{}{}\x16".format(chr(123), chr(primeAdress), chr(cs))
        return RequestShortFrame
        
    def getAllData(self, primeAdress):
        self.s.send(self.getDataDeviceCode(self.addr).encode())
        respond = self.s.recv(119)
        return respond
        
    def request(self):
        pass
        
    def setStop(self):
        self.stop = False

    def setStart(self):
        self.stop = True

    def setExit(self):
        self.exit = False

    def __exit__(self):
        self.s.close()
        
class Server(threading.Thread, observe.Observable):

    def __init__(self, host = '', port = 5005):
        threading.Thread.__init__(self)
        observe.Observable.__init__(self)
        self.host = host
        self.port = port
        if error.printMessages:
            print ('init Server Connection')
        threading.Thread.start(self)

    def run(self):
        #self.lock.acquire()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
        if error.printMessages:
            print ('Server Network listing')
        self.s.listen(1)
        if error.printMessages:
            print('Server Connection ist done')
        try:
            self.conn, self.addr = self.s.accept()
            # self.lock.release()
            self.request()
            
            #while self.exit:#threat wird erst beendet wenn aus while schleife herausgeganen wird
            #    if self.stop:
            #        self.request()
            #    time.sleep(1)
                #self.lock.release()self.request()

        except:
            print ("Fehler aufgetreten...")

        #finally:
            #self.s.close()

    def request(self):
        if error.printMessages:
            print ('Connected by', self.addr)
        
    def setStop(self):
        self.stop = False

    def setStart(self):
        self.stop = True

    def setExit(self):
        self.exit = False

    def __exit__(self):
        self.s.close()