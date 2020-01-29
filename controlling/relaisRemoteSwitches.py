
from connections import gbioRPIConnection
from observer import observe
import datetime

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

    def request(self):
        try:
            status = self.getGPIOPinStatus()
            self.dataStr = "{:8.6f}".format(status)
            message = self.getControlParameter()
            print (message)
            
        except:
            print ("GBIO controlled Ralais is not working!")
        
    def getData(self):
        return self.dataStr