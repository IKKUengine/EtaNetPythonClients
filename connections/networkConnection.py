import time
import threading
import socket
import error

from observer import observe

class MBusConnection(threading.Thread):
    exit = True
    stop = True
    

    def __init__(self, host = '192.168.178.66', port = 10001, primeAdress = 1):

        self.host = host
        self.port = port
        self.addr = primeAdress

        try: 
            if error.printMessages:
                print ('init MBus Connection')
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          
            if error.printMessages:
                print ("socket successfully created")       
            self.s.connect((self.host, self.port))
            if error.printMessages:
                print('Connection Mbus is done')
            self.initDevice(primeAdress)
            
            if error.printMessages:
                host_id = self.s.getpeername()
                print ("Addr.: " + str(host_id))
                print ("(\'" + host + "\', " + str(port) + ")")
                
            threading.Thread.__init__(self)
            threading.Thread.start(self)
            
        except:          
            print("socket NOT created")

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
        
class etaNetClient(threading.Thread, observe.Observable):
    exit = True
    stop = True
    
    def __init__(self, host = '192.168.178.22', port = 5005):

        self.host = host
        self.port = port

        try:
            threading.Thread.__init__(self)
            observe.Observable.__init__(self)
            if error.printMessages:
                print ('init Client Connection')
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          
            if error.printMessages:
                print ("Client socket successfully created")       
            
            
            if error.printMessages:
                host_id = self.s.getpeername()
                print ("Addr.: " + str(host_id))
                print ("(\'" + host + "\', " + str(port) + ")")        

            threading.Thread.start(self)
            
        except:          
            print("NO EtaNet Connection to the server. Please check the server or connection!")
        #finally:
            #self.s.close()
            
    def run(self):
        try:
            self.s.connect((self.host, self.port))
            print ("Connection etaNet is done")
            #self.s.send("t".encode())
        except:          
            print("NO EtaNet Connection to the server. Please check the server or connection!")
            #if error.printMessages:
             #   print('Connection Client is done')
       # while self.exit:#threat wird erst beendet wenn aus while schleife herausgeganen wird
       #     if self.stop:
       #         self.request()
       #     time.sleep(1)
       
    def sendAllData(self):
        message = error.systemIdentifier + ": " + str(self.getDataList())   
        lenString = len(message)
        if error.printMessages:  
            print (str(lenString))
            print (message)
        try:
            self.s.send(str(lenString).encode())
            self.s.send(message.encode())
        except:          
            print("NO EtaNet Connection to the server. Please check the server or connection!")
        #respond = self.s.recv(119)
        #return respond
        
    def setStop(self):
        self.stop = False

    def setStart(self):
        self.stop = True

    def setExit(self):
        self.exit = False

    def __exit__(self):
        self.s.close()