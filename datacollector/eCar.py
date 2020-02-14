from observer import observe
from connections import canConnection
from datacollector import eCar_BMW_i3
import parameter
import datetime
import re

class ECar(canConnection.CANConnection, observe.Observer):

    dataStr = "'NaN', 'NaN'"
    headerStr = "'SoC [%]', 'SoH [%]'"
 

    def __init__(self, observable):
       # rs232Connection.Rs232Connection.__init__()
        #observe.Observer.__init__(observable)
        canConnection.CANConnection.__init__(self)
        observe.Observer.__init__(self, observable)

        try:
            self.getSerialPort().write(str.encode('FORM:PH ALL\n'))  # ???
            self.getSerialPort().write(str.encode('CURR:SC +1.0e-1\n'))  # ???
            #Regular expression operations to find all scientific numbers
        except:
            pass

    def notifyData(self):
      return self.dataStr
    
    def notifyHeader(self):
      return self.headerStr

    def request(self):
        
        try:
            self.getSerialPort().write(str.encode('POW:ACT:AC?\n'))  # ???
            
            while True:
                SoC = eCar_BMW_i3.SoC_value()
                time.sleep(1)    # ???
                
                SoH = eCar_BMW_i3.SoH_value()
                time.sleep(1)    # ???
            
            self.dataStr = "{:8.6f}, {:8.6f}".format(SoC, SoH)  # ???
                
        except:
            print ("No connection to the eCar!")
            
    def getData(self):
        return self.dataStr