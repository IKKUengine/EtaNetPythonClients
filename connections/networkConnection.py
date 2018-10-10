import time
import threading
import socket

from observer import observe

class Client(threading.Thread, observe.Observable):
    exit = True
    stop = True

    def __init__(self, host = '192.168.178.66', port = 10001):
        threading.Thread.__init__(self)
        observe.Observable.__init__(self)
        self.host = host
        self.port = port
        print ('init NetworkConnection')
        threading.Thread.start(self)

    def run(self):
        #self.lock.acquire()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))
        print('Connection ist done')
            
        while self.exit:#threat wird erst beendet wenn aus while schleife herausgeganen wird
            if self.stop:
                self.request()
            time.sleep(1)

        #except:
            #print ("Fehler aufgetreten...")

        #finally:
            #self.s.close()

    def getData(self):
        #Hex-codierung
        self.s.sendall('')
        data = s.recv(119)
        return data
        
    
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

    def __init__(self, host, port):
        threading.Thread.__init__(self)
        observe.Observable.__init__(self)
        self.host = host
        self.port = port
        print ('init NetworkConnection')
        threading.Thread.start(self)

    def run(self):
        #self.lock.acquire()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
        print ('Network listing')
        self.s.listen(1)
        print('Connection ist done')
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
        print ('Connected by', self.addr)
        
    def setStop(self):
        self.stop = False

    def setStart(self):
        self.stop = True

    def setExit(self):
        self.exit = False

    def __exit__(self):
        self.s.close()