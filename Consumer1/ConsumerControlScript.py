import socket
import datetime
import re
import time
import meterbus
import pigpio
import threading
import PID
import xlrd
import csv

pi = pigpio.pi()

global mixing_pid 
host = '192.168.178.66'
port = 10001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
powerTs = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def initDevice(primeAdress):
    #self.s.send("\x10\x40\x01\x41\x16".encode())
    self.s.send(self.getInitDeviceCode(primeAdress).encode())
    if parameter.printMessages:
        print('Mbus init data are sent')
    respond = self.s.recv(1)
    if respond == b'\xe5':
        if parameter.printMessages:
            print('Mbus init war erfolgreich!!!')
    else:
        print('MBus init NICHT erfolgreich!!!')

def getInitDeviceCode(primeAdress):
    cs = 64 + primeAdress
    RequestShortFrame = "\x10\x40{}{}\x16".format(chr(primeAdress), chr(cs))
    return RequestShortFrame

def getDataDeviceCode(primeAdress):
    cs = 123 + primeAdress
    RequestShortFrame = "\x10{}{}{}\x16".format(chr(123), chr(primeAdress), chr(cs))
    return RequestShortFrame
    
def getAllData(primeAdress):
    s.send(getDataDeviceCode(primeAdress).encode())
    respond = s.recv(119)
    return respond

#excel read data

def readData():
    for r in range(1,42):
        data = (sheet.cell_value(r,0))
        global massflowrate_pid
        massflowrate_pid=pid_define("1","0.1","0.01",data,"10")
        time.sleep(3600)
        
# PID define

class pid_define:
    def __init__(self, proportional, integral, differential, setWantedParameter, setSampleTime):
        threading.Thread.__init__(self)
        self.proportional=float(proportional)
        self.integral=float(integral)
        self.differential=float(differential)
        self.setWantedParameter=float(setWantedParameter)
        self.pid = PID.PID(self.proportional, self.integral,self.differential)
        self.pid.SetPoint = self.setWantedParameter
        self.pid.setSampleTime(float(setSampleTime))
        self.pid.SetKp = self.proportional
        self.pid.SetKi = self.integral
        self.pid.SetKd = self.differential

# PWM define

class actuator:
    def __init__(self, pi, gpio_pin, pwm_frequency, pwm_dutycycle):
        threading.Thread.__init__(self)
        self.pi = pi
        self.gpio_pin=gpio_pin
        self.pwm_frequency=pwm_frequency
        self.pwm_dutycycle=pwm_dutycycle
        self.pi.set_mode(gpio_pin, pigpio.OUTPUT)
        self.pi.set_PWM_frequency(gpio_pin, pwm_frequency)
        self.pi.set_PWM_dutycycle(gpio_pin, pwm_dutycycle)

       
mixing_pid=pid_define("1","0.2","0.01","15","10")

file_location = "/home/pi/Desktop/Consumer1/exceltest1.xlsx"
workbook = xlrd.open_workbook(file_location)
sheet = workbook.sheet_by_index(0)

def process():
    
    while True:
        addr1 = 1
        addr3 = 2
        addr2 = 3
        try:
            data1 = getAllData(addr1)
            telegram1 = meterbus.load(data1)
            data2 = getAllData(addr2)
            telegram2 = meterbus.load(data2)
            data3 = getAllData(addr3)
            telegram3 = meterbus.load(data3)    
        
            #Instabilities/bugs of meterbus lib/package
            #heatmeter1
            find1 = [float(x) for x in re.findall(match_number, str(telegram1.records[13].interpreted) + str(telegram1.records[13].interpreted))]
            if find1[0] == 3:
                flow1 = find1[1]
            else:
                flow1 = find1[0]

            powList1 = [float(x) for x in re.findall(match_number, str(telegram1.records[12].interpreted) \
                      + str(telegram1.records[13].interpreted) + str(telegram1.records[9].interpreted) \
                      + str(telegram1.records[10].interpreted))]
            #Heatmeter2
            find2 = [float(x) for x in re.findall(match_number, str(telegram2.records[13].interpreted) + str(telegram2.records[13].interpreted))]
            if find2[0] == 3:
                flow2 = find2[1]
            else:
                flow2 = find2[0]

            powList2 = [float(x) for x in re.findall(match_number, str(telegram2.records[12].interpreted) \
                      + str(telegram2.records[13].interpreted) + str(telegram2.records[9].interpreted) \
                      + str(telegram2.records[10].interpreted))]
            #Heatmeter3
            find3 = [float(x) for x in re.findall(match_number, str(telegram3.records[13].interpreted) + str(telegram3.records[13].interpreted))]
            if find3[0] == 3:
                flow3 = find3[1]
            else:
                flow3 = find3[0]

            powList3 = [float(x) for x in re.findall(match_number, str(telegram3.records[12].interpreted) \
                      + str(telegram3.records[13].interpreted) + str(telegram3.records[9].interpreted) \
                      + str(telegram3.records[10].interpreted))]
            
            dateNow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print (dateNow)
            
            heatMeter1 = powList1[0], flow1, powList1[3], powList1[4]
            heatMeter2 = powList2[0], flow2, powList2[3], powList2[4]
            heatMeter3 = powList3[0], flow3, powList3[3], powList3[4]
            
            H1_P = heatMeter1[0]
            print ("Heatmeter 1: Thermal power [W]",H1_P)
            H1_V = heatMeter1[1]
            print ("Heatmeter 1: Current Volumetric Flow Rate [m³/h]",H1_V)
            H1_T_Flow = heatMeter1[2]
            print ("Heatmeter 1: Current Flow Temperature [°C]",H1_T_Flow)
            H1_T_Return = heatMeter2[3]
            print ("Heatmeter 1: Current Return Temperature [°C]",H1_T_Return)

            H2_P = heatMeter2[0]
            print ("Heatmeter 2: Thermal power [W]",H2_P)
            H2_V = heatMeter2[1]
            print ("Heatmeter 2: Current Volumetric Flow Rate [m³/h]",H2_V)
            H2_T_Flow = heatMeter2[2]
            print ("Heatmeter 2: Current Flow Temperature [°C]",H2_T_Flow)
            H2_T_Return = heatMeter2[3]
            print ("Heatmeter 2: Current Return Temperature [°C]",H2_T_Return)

            H3_P = heatMeter3[0]
            print ("Heatmeter 3: Thermal power [W]",H3_P)
            H3_V = heatMeter3[1]
            print ("Heatmeter 3: Current Volumetric Flow Rate [m³/h]",H3_V)
            H3_T_Flow = heatMeter3[2]
            print ("Heatmeter 3: Current Flow Temperature [°C]",H3_T_Flow)
            H3_T_Return = heatMeter3[3]
            print ("Heatmeter 3: Current Return Temperature [°C]",H3_T_Return)
            
            mixing_pid.pid.update(H3_T_Flow)
            massflowrate_pid.pid.update(H3_P)
            print("Temperature Set Value [°C]",mixing_pid.setWantedParameter)
            print("Energy Set Value [W]",massflowrate_pid.setWantedParameter)
            
            header = ['Datetime', 'Heatmeter 1 Energy(W)', 'Heatmeter 1 Volumetric Flow(m3/h)', 'Heatmeter 1 Flow Temperature(°C)', 'Heatmeter 1 Return Temperature(°C)', 'Heatmeter 2 Energy(W)', 'Heatmeter 2 Volumetric Flow(m3/h)', 'Heatmeter 2 Flow Temperature(°C)', 'Heatmeter 2 Return Temperature(°C)', 'Heatmeter 3 Energy(W)', 'Heatmeter 3 Volumetric Flow(m3/h)', 'Heatmeter 3 Flow Temperature(°C)', 'Heatmeter 3 Return Temperature(°C)']
            
            with open('/home/pi/Desktop/heatmeter_readings.csv', mode='a') as heatmeter_readings:
                heatmeter_write = csv.writer(heatmeter_readings)
                #heatmeter_write.writerow(i for i in header)
                write_to_log = heatmeter_write.writerow([dateNow, H1_P, H1_V, H1_T_Flow, H1_T_Return, H2_P, H2_V, H2_T_Flow, H2_T_Return, H3_P, H3_V, H3_T_Flow, H3_T_Return, mixing_pid.setWantedParameter, massflowrate_pid.setWantedParameter])

           
            if H3_T_Flow != mixing_pid.setWantedParameter: 
                if mixing_pid.pid.output < 0:
                    x = abs(mixing_pid.pid.output)
                    setPWM_1 = x 
                    print ("PID -1- Value",x)
                    setPWM_1 = max(min( int(setPWM_1), 255),0)
                    print ("PWM -1- Value",setPWM_1)

                else:
                    pass
            else:
                pass
            
            if H3_P != massflowrate_pid.setWantedParameter:
                if 100 <= massflowrate_pid.setWantedParameter <= 300:
                    setPWM_2 =massflowrate_pid.pid.output
                    print ("PID -2- Value",massflowrate_pid.pid.output)
                    setPWM_2 = max(min( int(setPWM_2), 19),0)
                    print ("PWM -2- Value",setPWM_2)
                    massflowrate_actuator=actuator(pi,12,1000,setPWM_2)
                
                if 400 <= massflowrate_pid.setWantedParameter <= 600:
                    setPWM_2 =massflowrate_pid.pid.output
                    print ("PID -2- Value",massflowrate_pid.pid.output)
                    setPWM_2 = max(min( int(setPWM_2), 28),0)
                    print ("PWM -2- Value",setPWM_2)
                    massflowrate_actuator=actuator(pi,12,1000,setPWM_2)
                
                if 500 <= massflowrate_pid.setWantedParameter <= 900:
                    setPWM_2 =massflowrate_pid.pid.output
                    print ("PID -2- Value",massflowrate_pid.pid.output)
                    setPWM_2 = max(min( int(setPWM_2), 36),0)
                    print ("PWM -2- Value",setPWM_2)
                    massflowrate_actuator=actuator(pi,12,1000,setPWM_2)
                
                if 1000 <= massflowrate_pid.setWantedParameter <= 3000:
                    setPWM_2 =massflowrate_pid.pid.output
                    print ("PID -2- Value",massflowrate_pid.pid.output)
                    setPWM_2 = max(min( int(setPWM_2), 42),0)
                    print ("PWM -2- Value",setPWM_2)
                    massflowrate_actuator=actuator(pi,12,1000,setPWM_2)
                
                if 4000 <= massflowrate_pid.setWantedParameter <= 6000:
                    setPWM_2 =massflowrate_pid.pid.output
                    print ("PID -2- Value",massflowrate_pid.pid.output)
                    setPWM_2 = max(min( int(setPWM_2), 50),0)
                    print ("PWM -2- Value",setPWM_2)
                    massflowrate_actuator=actuator(pi,12,1000,setPWM_2)
                    
                if 7000 <= massflowrate_pid.setWantedParameter <= 9000:
                    setPWM_2 =massflowrate_pid.pid.output
                    print ("PID -2- Value",massflowrate_pid.pid.output)
                    setPWM_2 = max(min( int(setPWM_2), 58),0)
                    print ("PWM -2- Value",setPWM_2)
                    massflowrate_actuator=actuator(pi,12,1000,setPWM_2)
                
                if massflowrate_pid.setWantedParameter > 10000:
                    setPWM_2 =massflowrate_pid.pid.output
                    print ("PID -2- Value",massflowrate_pid.pid.output)
                    setPWM_2 = max(min( int(setPWM_2), 64),0)
                    print ("PWM -2- Value",setPWM_2)
                    massflowrate_actuator=actuator(pi,12,1000,setPWM_2)
            else:
                pass
            
            time.sleep(5)
        except:
            print("doing nothing")
        
                    
thread_readData=threading.Thread(target=readData)
thread_process=threading.Thread(target=process)

thread_readData.start()
thread_process.start()

thread_readData.join()
thread_process.join()

pi.stop()        

    