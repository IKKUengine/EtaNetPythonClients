
from connections import gbioRPIConnection
from observer import observe
import datetime
import parameter

class RemoteSwitches (gbioRPIConnection.OnePortGbioRpiConnection, observe.Observer, observe.Observable):

    dataStr = "'NaN'"
    headerStr = "'CHP On/Off'"

    def __init__(self, observable):
        gbioRPIConnection.OnePortGbioRpiConnection.__init__(self, 12)
        observe.Observer.__init__(self, observable)
        observe.Observable.__init__(self)
        
    def notifyData(self):
        return self.dataStr
    
    def notifyHeader(self):
      return self.headerStr
    
    def notifyControl(self):
      return self.headerStr
    
    def request(self):
        #try:
        message = parameter.control_parameter
        print ("Länge: {:8.6f}".format(len(message)))
        if len(message) == 6:     
            print("ONOFF:")
            print (message)
            if int(message[0]) == 0:
                print("Off CHP")
                self.setGPIOPinOff()
            else:
                print("ON CHP")
                self.setGPIOPinOn()
        status = self.getGPIOPinStatus()
        print(status)
        self.dataStr = "{:8.6f}".format(status)
            
        #except:
         #   print ("GBIO controlled Ralais is not working!")
        
    def getHeader(self):
        return self.headerStr
    
    def getData(self):
        return self.dataStr