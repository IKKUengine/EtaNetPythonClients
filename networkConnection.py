import time
import threading
import socket
import parameter
from PySide import QtNetwork, QtCore, QtGui
import re
import datetime

from observer import observe

class MBusConnection(threading.Thread):
    exit = True
    stop = True
    

    def __init__(self, host = '192.168.178.66', port = 10001):

        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        try:                       
            self.s.connect((self.host, self.port))
            threading.Thread.__init__(self)
            threading.Thread.start(self)
            
        except:          
            print("socket NOT created")

    def run(self):  
        while self.exit:
            if self.stop:
                self.request()
            time.sleep(parameter.timeTriggerMeterbus)
                
    def request(self):
        pass
     
    def initDevice(self, primeAdress):
        #self.s.send("\x10\x40\x01\x41\x16".encode())
        self.s.send(self.getInitDeviceCode(primeAdress).encode())
        if parameter.printMessages:
            print('Mbus init data are sent')
        respond = self.s.recv(1)
        if respond == b'\xe5':
            if parameter.printMessages:
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
        print(primeAdress)
        self.s.send(self.getDataDeviceCode(primeAdress).encode())
        respond = self.s.recv(119)
        return respond 
    
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
    messageServer = "NO SERVER CONNECTION!"
    feedback = "Ready to get feedback!"
    
    def __init__(self, host = '192.168.178.20', port = 50005):

        self.host = host
        self.port = port

        #print(host)
        observe.Observable.__init__(self)
        threading.Thread.__init__(self)

        threading.Thread.start(self)
        
    def run(self):
        while self.exit:
            if self.stop:
                self.notify_observersMonitoring()
                time.sleep(parameter.timeTriggerSendData)
                self.sendAllData()
       
    def setIP(self, host):
        self.host = host
        
    def getIP(self):
        return self.host    
    
    def sendAllData(self):
        #match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
        #match_number = re.compile("[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?")
        powerTs = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message =  "'{}' ('TimeStamp', {}) VALUES ('{}', {})".format(parameter.systemIdentifier, self.getHeaderList(), powerTs , self.getDataList()) 
            
        try:
            newList = [] 
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#,socket.SO_REUSEADDR, socket.SO_REUSEPORT)
            self.s.connect((self.host, self.port))
            block = QtCore.QByteArray()
            out = QtCore.QDataStream(block, QtCore.QIODevice.WriteOnly)
            out.setVersion(QtCore.QDataStream.Qt_4_0)  
            
            out.writeQString(message)
            #print(message)
            self.s.send(block.data())
            print (message)
           # self.messageServer = "NO SERVER CONNECTED!"
            block2 = QtCore.QByteArray()
            into = QtCore.QDataStream(block2, QtCore.QIODevice.ReadWrite)
            into.setVersion(QtCore.QDataStream.Qt_4_0)
            message = self.s.recv(1024)
            byteMessageList = list(message.decode('ascii'))
            strMessage = ''.join(str(x) for x in byteMessageList)
            strMessageList = strMessage.split(";")
            for i in strMessageList:
               newList.append( str(i.split(chr(0))).replace(' ', '').replace(',', '').replace(']', '').replace('[', '').replace("'", ''))
            newList[0] = str(re.findall(r'\d+\.*\d*', newList[0])).replace("'", '').replace(']', '').replace('[', '')
            self.s.close()
            #print(byteMessageList)
            if byteMessageList[5] == 'E' and  byteMessageList[7] == '5':
                self.feedback = "None of the disturbance parameters has changed (E5). ({}).".format(self.getControlParameter())

            elif byteMessageList[5] == 'E' and  byteMessageList[7] == '6':
                #Aktion bwz. Controlling
                self.feedback = "Wrong messages from client. Data structure does not correspond to the protocol (E6)."                
            elif byteMessageList[5] == 'E' and  byteMessageList[7] == '7':
                #Aktion bwz. Controlling
                self.feedback = "Data structure does not correspond to the protocol or database on the server is locked by another app (E7)."
                
            elif byteMessageList[5] == 'E' and  byteMessageList[7] == '8':
                #Aktion bwz. Controlling
                self.feedback = "Servers did not receive any messages or the message was empty (E8)."
                     
            else:
               self.setControlParameter(newList)
               parameter.control_parameter = newList
               print(self.getControlParameter()) 
               self.feedback = "Server feedback: Client is configured! ({}).".format(self.getControlParameter())

              
            self.messageServer = "SERVER CONNECTED!"
            #print("SERVER CONNECTED!")
        except:
            if parameter.printMessages:
                print ("Please switch on the Server-App!")
            self.messageServer = "NO SERVER CONNECTED!"
            #print("NO SERVER CONNECTED!")

        
    def setStop(self):
        self.stop = False

    def setStart(self):
        self.stop = True

    def setExit(self):
        self.exit = False
    
    def getMessageServer(self):
        return self.messageServer
    
    def getFeedback(self):
        return self.feedback

    def __exit__(self):
        self.messageServer = "NO SERVER CONNECTED!"
        self.s.close()