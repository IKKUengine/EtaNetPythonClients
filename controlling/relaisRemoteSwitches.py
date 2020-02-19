
from connections import gbioRPIConnection
from observer import observe
import datetime

class RemoteSwitches (gbioRPIConnection.OnePortGbioRpiConnection, observe.Observer, observe.Observable):

    dataStr = "'NaN',  'NaN'"
    headerStr = "'Load Enable eCar On/Off', 'Load Enable'"

    def __init__(self, observable):
        gbioRPIConnection.OnePortGbioRpiConnection.__init__(self, 12)
        observe.Observer.__init__(self, observable)
        observe.Observable.__init__(self)
        
    def notifyData(self):
        return self.dataStr
    
    def notifyHeader(self):
      return self.headerStr

    def request(self):
        #try:
        statusECarONOFF = self.getGPIOPinStatus1()
        statusLoadEnable = self.getGPIOPinStatus2()
        self.dataStr = "{:8.6f}, {:8.6f}".format(statusECarONOFF, statusLoadEnable)
        message = self.getControlParameter()
        print (message)
            
        #except:
            #print ("GBIO controlled Ralais is not working!")
        
    def getData(self):
        return self.dataStr