from observer import observe
from connections import rs232Connection
import parameter
import datetime
import re

class PowerAnalyzer(rs232Connection.Rs232Connection, observe.Observer):

    dataStr = "(TimeStamp; Power Analyser; Value1; Unit1; Value2; Unit2)"

    def __init__(self, observable):
       # rs232Connection.Rs232Connection.__init__()
        #observe.Observer.__init__(observable)
        rs232Connection.Rs232Connection.__init__(self)
        observe.Observer.__init__(self, observable)
        self.getSerialPort().write(str.encode('FORM:PH ALL\n'))
        self.getSerialPort().write(str.encode('CURR:SC +1.0e-1\n'))
        #Regular expression operations to find all scientific numbers
        self.match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')

    def notify(self):
      return self.dataStr

    def request(self):
        if True: #parameter.printMessages:
            #For the perfomance voltage and current are only switched on for diagnostic purposes.
            self.getSerialPort().write(str.encode('VOLT:RMS:AC?\n'))
            data1 = self.getSerialPort().read(35)
            
            self.getSerialPort().write(str.encode('CURR:RMS:AC?\n'))
            data2 = self.getSerialPort().read(35)
            
            self.getSerialPort().write(str.encode('FREQ?\n'))
            data4 = self.getSerialPort().read(35)
            
            voltList = [float(x) for x in re.findall(self.match_number, str(data1))]
            currList = [float(x) for x in re.findall(self.match_number, str(data2))]
            freqList = [float(x) for x in re.findall(self.match_number, str(data4))] 
        
        self.getSerialPort().write(str.encode('POW:ACT:AC?\n'))
        data3 = self.getSerialPort().read(35)
        powerTs = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")       
        powList = [float(x) for x in re.findall(self.match_number, str(data3))]      
        
        if parameter.printMessages:       
            print ("Datetime: " + powerTs)
            print ("Voltage L1,L2,L3: " + str(voltList) + " [V]")
            print ("Current L1,L2,L3: " + str(currList) + " [A]")
            print ("Power L1,L2,L3: " + str(powList) + " [W]")
            print ("Frequency L1,L2,L3: " + str(freqList) + " [Hz]")
        try:
            self.dataStr = "({}; Power Analyser; {}; {}; {}; {}; {}; {})".format(powerTs, powList[0], \
                           "[L1, W]", powList[1], "[L2, W]", powList[2], "[L3, W]")
        except:
            print ("Power Analyser is switched off!")
            
    def getData(self):
        return self.dataStr