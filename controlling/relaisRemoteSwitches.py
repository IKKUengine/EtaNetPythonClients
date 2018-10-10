
from connections import gbioRPIConnection
from observer import observe

class RemoteSwitches (gbioRPIConnection.GbioRpiConnection, observe.Observer):

    dataStr = "(TimeStamp; CHP ON/OFF; Value1; Unit1; Value2; Unit2)"

    def __init__(self, observable):
        # rs232Connection.Rs232Connection.__init__()
        #observe.Observer.__init__(observable)
        gbioRPIConnection.GbioRpiConnection.__init__(self)
        observe.Observer.__init__(self, observable)
        
    def notify(self):
        return self.dataStr

    def request(self):
        pass

