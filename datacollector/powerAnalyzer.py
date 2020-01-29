from observer import observe
from connections import rs232Connection
import parameter
import datetime
import re

class PowerAnalyzer(rs232Connection.Rs232Connection, observe.Observer):

    dataStr = "'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN'"
    headerStr = "'El_Power_L1 [W]', 'El_Power_L2 [W]', 'El_Power_L3 [W]', 'Voltage_L1 [V]', 'Voltage_L2 [V]', 'Voltage_L3 [V]', 'Current_L1 [A]', 'Current_L2 [A]', 'Current_L3 [A]', 'Frequency_L1 [Hz]', 'Frequency_L2 [Hz]', 'Frequency_L3 [Hz]'"
 

    def __init__(self, observable):
       # rs232Connection.Rs232Connection.__init__()
        #observe.Observer.__init__(observable)
        rs232Connection.Rs232Connection.__init__(self)
        observe.Observer.__init__(self, observable)
        self.match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')

        try:
            self.getSerialPort().write(str.encode('FORM:PH ALL\n'))
            self.getSerialPort().write(str.encode('CURR:SC +1.0e-1\n'))
            #Regular expression operations to find all scientific numbers
        except:
            pass

    def notifyData(self):
      return self.dataStr
    
    def notifyHeader(self):
      return self.headerStr

    def request(self):
        
        try:
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
                print ("Voltage L1,L2,L3: " + str(voltList) + " v")
                print ("Current L1,L2,L3: " + str(currList) + " [A]")
                print ("Power L1,L2,L3: " + str(powList) + " [W]")
                print ("Frequency L1,L2,L3: " + str(freqList) + " [Hz]")
            
            self.dataStr = "{:8.6f}, {:8.6f}, {:8.6f}, {:8.6f},{:8.6f}, {:8.6f}, {:8.6f}, {:8.6f},{:8.6f}, {:8.6f}, {:8.6f}, {:8.6f}".format(powList[0], powList[1], powList[2], voltList[0], voltList[1], voltList[2], currList[0], currList[1], currList[2],freqList[0], freqList[1], freqList[2])
                
        except:
            print ("Power Analyser is switched off!")
            
    def getData(self):
        return self.dataStr