
from connections import gbioRPIConnection
from observer import observe
import datetime

class RemoteSwitches (gbioRPIConnection.GbioRpiConnection, observe.Observer):

    dataStr = "(TimeStamp; CHP ON/OFF; Value1; Unit1; Value2; Unit2)"

    def __init__(self, observable):
        gbioRPIConnection.GbioRpiConnection.__init__(self)
        observe.Observer.__init__(self, observable)
        
    def notify(self):
        return self.dataStr
    

    def request(self):
        powerTs = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = self.getCHPOnOffStatus()
        try:
            self.dataStr = "({}; CHP On/Off; {}; {})".format(powerTs, status, "[None]")       
        except:
            print ("Gas Mass Flow Sensor is switched off!")

    def getData(self):
        return self.dataStr