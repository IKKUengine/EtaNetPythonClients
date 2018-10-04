import threading
import socket

from observer import observe

class NetworkConnection(threading.Thread, observe.Observable):

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

        except:
            print ("Fehler aufgetreten...")

        #finally:
            #self.s.close()

    def request(self):
        print ('Connected by', self.addr)

    def __exit__(self):
        self.s.close()