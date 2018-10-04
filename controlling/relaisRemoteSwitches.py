from connections import gbioRPIConnection
from observer import observe

class RemoteSwitches (gbioRPIConnection.GbioRpiConnection, observe.Observer):

    dataStr = "(TimeStamp; SensorName; Value; Unit; Value; Unit; ...)"
    #ToDo: ReceiveData() hier werden keine Daten gesendet sondern empfangen
    def notify(self):
        return self.dataStr

    def request(self):
        if GPIO.input(12):
            self.signalText['text'] = 'CHP is OFF'
        else:
            self.signalText['text'] = 'CHP is ON'
        GPIO.output(12, not GPIO.input(12))
