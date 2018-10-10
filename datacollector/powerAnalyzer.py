
from observer import observe
from connections import rs232Connection

class PowerAnalyzer(rs232Connection.Rs232Connection, observe.Observer):

    dataStr = "(TimeStamp; Power Analyser; Value1; Unit1; Value2; Unit2)"

    def __init__(self, observable):
       # rs232Connection.Rs232Connection.__init__()
        #observe.Observer.__init__(observable)
        rs232Connection.Rs232Connection.__init__(self)
        observe.Observer.__init__(self, observable)

    def notify(self):
      return self.dataStr

    def request(self):
        print ("done power analyser")
        # t=Thread(target=self.masurementRunning, args=()).start()
        # self.ser.write(str.encode('FORM:PH L1\n'))
        # self.ser.write(str.encode('VOLT:RMS:AC?\n'))
        # ser.write(str.encode('CURR:RMS:AC?\n'))
        # ser.write(str.encode('POW:FAC:AC?\n'))
        # data1 = self.ser.read(10) #Read 10 characters from serial port to data
        #self.ser.write(str.encode('POW:ACT:AC?\n'))
        # data2 = self.ser.read(15)

        # ser.write(str.encode('POW:ACT:AC? FORM:PH L1?\n'))
        # data3 = ser.read(40)

        # ser.write(str.encode('POW:ACT:AC? FORM:PH L2?\n'))
        # data4 = ser.read(40)

        # ser.write(str.encode('POW:ACT:AC? FORM:PH L3?\n'))
        # data5 = ser.read(40)

        # self.ser.write(str.encode('FORM:PH L3\n'))

        #self.ser.write(str.encode('VOLT:RMS:AC?\n'))
        # ser.write(str.encode('CURR:RMS:AC?\n'))
        # ser.write(str.encode('POW:FAC:AC?\n'))
        #data = self.ser.read(22)  # Read 10 characters from serial port to data

        # self.ser.write(str.encode('POW:ACT:AC?\n'))
        # data5 = self.ser.read(10)

        # ser.write(str.encode('POW:ACT:AC? FORM:PH L1?\n'))
        # data3 = ser.read(40)

        # ser.write(str.encode('POW:ACT:AC? FORM:PH L2?\n'))
        # data4 = ser.read(40)

        # ser.write(str.encode('POW:ACT:AC? FORM:PH L3?\n'))
        # data5 = ser.read(40)

        # ser.write(str.encode('FORM:PH L3\n'))
        # data6 = ser.read(100)

        # ser.write(str.encode('POW:ACT:AC?\n'))
        # data3 = ser.read(100)

        #self.infoText['text'] =  data
        #self.infoText['text'] =  "test 123"

        #self.ser.close