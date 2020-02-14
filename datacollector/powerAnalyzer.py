from observer import observe
from connections import rs232Connection
import parameter
import datetime
import re
import numpy

class PowerAnalyzer(rs232Connection.Rs232Connection, observe.Observer):

    dataStr = "'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN'"
    headerStr = "'T1 [°C]', 'T2 [°C]', 'T3 [°C]', 'T4 [°C]', 'T5 [°C]', 'TMax [°C]', 'TMin [°C]', 'Rel. Level [%]', 'Abs. Level [kWh]'"
    
    wire1='/sys/devices/w1_bus_master1/3b-2c98073da241/w1_slave'
    wire2='/sys/devices/w1_bus_master1/3b-2c98073db8b6/w1_slave'
    wire3='/sys/devices/w1_bus_master1/3b-4c98073d93cd/w1_slave'
    wire4='/sys/devices/w1_bus_master1/3b-4c98073d951d/w1_slave'
    wire5='/sys/devices/w1_bus_master1/3b-4cfc0958f8ce/w1_slave'
    q = 0
    q_rel = 0
    tMax = 73
    tMin = 12

    def __init__(self, observable):
       # rs232Connection.Rs232Connection.__init__()
        #observe.Observer.__init__(observable)
        rs232Connection.Rs232Connection.__init__(self)
        observe.Observer.__init__(self, observable)
        self.match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
        # Sensorpfade:


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
        
        t1 = self.temp_read(self.wire1)
        t2 = self.temp_read(self.wire2)
        t3 = self.temp_read(self.wire3)
        t4 = self.temp_read(self.wire4)
        t5 = self.temp_read(self.wire5)
        self.calc_heat(t1, t2, t3, t4, t5)
        print(self.getRelLevel())
        print("   ")
        print(self.getAbsLevel())
        try:           
            self.dataStr = "{:8.6f}, {:8.6f}, {:8.6f}, {:8.6f},{:8.6f}, {:8.6f}, {:8.6f}, {:8.6f},{:8.6f}".format(t1, t2, t3, t4, t5, self.tMax, self.tMin, self.q_rel, self.q)               
        except:
            print ("Temp. measurement is not work!")
            
    def getData(self):
        return self.dataStr
    
    def getHeader(self):
        return self.headerStr
    
    # Auslesend der Temperatur:
    def temp_read(self, pfad):
        value = 'NaN'
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
        cp=4.182
        roh=0.987
        V_ges=950
        V_1=20.8
        V_2=27.5
        V_3=18.1
        V_4=12.5
        V_5=20.8

        #q sollte die Energiemenge sein, die durch die Heatmeter bestimmt wird.
        #q, q_rel
        q_max=cp*roh*V_ges*(self.tMax)/3600
        q_min=cp*roh*V_ges*(self.tMin)/3600
        q_delta=cp*roh*V_ges*(self.tMax-self.tMin)/3600
        q1=cp*roh*(t1-self.tMin)*(V_1/100)*V_ges/3600
        q2=cp*roh*(t2-self.tMin)*(V_1/100)*V_ges/3600
        q3=cp*roh*(t3-self.tMin)*(V_1/100)*V_ges/3600
        q4=cp*roh*(t4-self.tMin)*(V_1/100)*V_ges/3600
        q5=cp*roh*(t5-self.tMin)*(V_1/100)*V_ges/3600
        self.q=q1+q2+q3+q4+q5
        self.q_rel=(self.q/q_delta)*100
    
    def getRelLevel(self):
        return self.q_rel
    
    def getAbsLevel(self):
        return self.q
