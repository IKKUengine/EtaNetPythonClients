
from connections import gbioRPIConnection
from observer import observe
import datetime
import parameter

class RemoteSwitches (gbioRPIConnection.OnePortGbioRpiConnection, observe.Observer, observe.Observable):

    dataStr = "'NaN'"
    headerStr = "'Load Enabe eCar On/Off'"

    def __init__(self, observable):
        gbioRPIConnection.OnePortGbioRpiConnection.__init__(self, 24)
        observe.Observer.__init__(self, observable)
        observe.Observable.__init__(self)
        
    def notifyData(self):
        return self.dataStr
    
    def notifyHeader(self):
      return self.headerStr

    def request(self):
#         try:
        message = parameter.control_parameter
        if len(message) == 6:     
            print("ONOFF:")
            print (message)
            if int(message[5]) == 0:
                print("Off eCar")
                self.setGPIOPinOff()
            else:
                print("ON eCar")
                self.setGPIOPinOn()
        status = self.getGPIOPinStatus()
        print(status)
        self.dataStr = "{:8.6f}".format(status)
            
#         except:
#             print ("GBIO controlled Ralais is not working!")
        
    def getData(self):
        return self.dataStr