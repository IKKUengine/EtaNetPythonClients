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
        # Sensorpfade:
        self.wire1='/sys/devices/w1_bus_master1/3b-2c98073da241/w1_slave'
        self.wire2='/sys/devices/w1_bus_master1/3b-2c98073db8b6/w1_slave'
        self.wire3='/sys/devices/w1_bus_master1/3b-4c98073d93cd/w1_slave'
        self.wire4='/sys/devices/w1_bus_master1/3b-4c98073d951d/w1_slave'
        self.wire5='/sys/devices/w1_bus_master1/3b-4cfc0958f8ce/w1_slave'

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
    
    # Auslesend der Temperatur:
    def temp_read(self, pfad):
        value = NaN
        with open(pfad) as f:
            f.readline()
            s=f.readline()
        n=s.find('t=')
        if(n>0):
            temp=int(s[n+2:])/1000
        return temp
    
    # Funktion zum Berechnen des Füllstands:
    def calc_heat (self,t1, t2, t3, t4, t5):
        #Configs of the Buffer and cal.
        cp=#float(config[0])
        roh=#float(config[1])
        V_ges=950
        V_1=#float(config[3])
        V_2=#float(config[4])
        V_3=#float(config[5])
        V_4=#float(config[6])
        V_5=#float(config[7])
        t_min= 12#float(config[8])
        t_max= 73#float(config[9])
        #q sollte die Energiemenge sein, die durch die Heatmeter bestimmt wird.
        q, q_rel
        q_max=cp*roh*V_ges*(t_max)/3600
        q_min=cp*roh*V_ges*(t_min)/3600
        q_delta=cp*roh*V_ges*(t_max-t_min)/3600
        q1=cp*roh*(t1-t_min)*(V_1/100)*V_ges/3600
        q2=cp*roh*(t2-t_min)*(V_1/100)*V_ges/3600
        q3=cp*roh*(t3-t_min)*(V_1/100)*V_ges/3600
        q4=cp*roh*(t4-t_min)*(V_1/100)*V_ges/3600
        q5=cp*roh*(t5-t_min)*(V_1/100)*V_ges/3600
        q=q1+q2+q3+q4+q5
        q_rel=(q/q_delta)*100
        return q_rel
