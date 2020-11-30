import time
import threading
import parameter
import datetime
import json, requests
import cayenne.client 
import numpy as np

from observer import observe
from connections import gpsConnection

class WeatherServer(threading.Thread):
    exit = True
    stop = True
    
    def __init__(self):

        try:
            
            threading.Thread.__init__(self)
            threading.Thread.start(self)

        except:
            print("Weather thread can not start!")

    def run(self):  
        while self.exit:
            if self.stop:
                self.request()
            time.sleep(parameter.timeTriggerMeterbus)
            
                
    def request(self):
        pass
     
        
    def getAPI(self):
        #request from GPS
#         geo=self.getGeo()
#         lat=self.getLat(geo)
#         lon=self.getLon(geo)
        lat=49.02093816
        lon=8.389365667
        key = 'd1460eff29e117c1a377c77c7d9071c4'
        units = 'metric'
        url = requests.get('http://api.openweathermap.org/data/2.5/weather?lat='+str(lat)+'&lon='+str(lon)+'&units='+units+'&appid='+key)
        weather = json.loads(url.text)
        return weather
    
        #Weather API Functions
    def getWeather(self,weather):
        weatherDesc= weather['weather'][0]['description']
        return weatherDesc

    def getPressure(self,weather):
        Pout = (weather['main']['pressure']*100)/1000
        return Pout
     
    def getTempOut(self,weather):
        Tout = weather['main']['temp']
        return Tout
    
    def setStop(self):
        self.stop = False

    def setStart(self):
        self.stop = True

    def setExit(self):
        self.exit = False

    def __exit__(self):
        pass
        
        
class CloudConnection(threading.Thread, observe.Observable):
    
    exit = True
    stop = True
    messageServer = "NO CLOUD CONNECTION!"
    feedback = "Ready to get feedback!"
    carMode = 1
    startLevel = 0
    airCondition = 0
    tempIn = 0
    desTemp = 0
    speed0 = 0.0
    alt0 = 0
    cAC = []
    message = "0, 0, 0, 0, 0, 0, 0, 0, 0, 0"

    def __init__(self):

        observe.Observable.__init__(self)
        threading.Thread.__init__(self)
         
        MQTT_USERNAME  = "20892060-92f2-11ea-93bf-d33a96695544"
        MQTT_PASSWORD  = "b64c0d13e163f20801cabdfd935acefc581b897d"
        MQTT_CLIENT_ID = "31a52d60-d7e6-11ea-a67f-15e30d90bbf4"
          
        self.client = cayenne.client.CayenneMQTTClient()
#         self.client.on_message = on_message(message)
        self.client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)

        threading.Thread.start(self)
        
    # The callback for when a message is received from Cayenne.
#     def on_message(self,message):
#       print("message received: " + str(message))
    # If there is an error processing the message return an error string, otherwise return nothing.
    
    def run(self):
        while self.exit:
            if self.stop:
                self.notify_observersMonitoring()
                time.sleep(parameter.timeTriggerSendData)
                self.sendAllData()
       
    def setCarMode(self, mode):
        self.carMode = mode

    def setTempIn(self, carTemp):
        self.tempIn = carTemp
      
    def setStartLevelBattery(self, startLevel):
        self.startLevel = startLevel
        return self.startLevel
        
    def setAirCondition(self, cc):     
        self.airCondition = cc
    
    def sendAllData(self):

        datetimeCloud = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message =  "'{}' ('TimeStamp', {}) VALUES ('{}', {})".format(parameter.systemIdentifier, self.getHeaderList(), datetimeCloud , self.getDataList()) 
        print("sendAllData Message : ", message)
        self.getDataList()
        self.mqttData(self.getDataList())
        self.messageServer = "WITH IoT-CLOUD CONNECTED!"
    
    def mqttData(self, dataString):
        dataList = dataString.split(',')
        print('dataLIST MQTTDATA', dataList)
        if len(dataList) >=8:
            #bring ot datalist
            tempOut = dataList[0]
            pressure = dataList[1]
            weatherDescription = dataList[2]
            tempSensor = dataList[3] 
            lon = dataList[4]
            lat = dataList[5]
            speed = dataList[6]
            alt = dataList[7]
            
            #calculate power, energy and battery level
            power = self.power(speed, self.speed0, alt, self.alt0, tempOut, pressure, self.carMode, self.airCondition, self.tempIn, self.cAC, self.desTemp)
            energyConsumption = self.energyConsumption(power, speed)
            energyIns = self.energyIns(power)
            startingEnergy =  (37.9/100)*self.startLevel 
            self.startLevel = (100/37.9) * self.batteryEnergy(startingEnergy, energyIns) #something wrong here
            
            #publish data to Cayenne cloud
            self.client.loop()
            self.client.virtualWrite(23, lat,"analog_sensor","null")
            self.client.virtualWrite(17, lon,"analog_sensor","null")
            self.client.virtualWrite(5, tempSensor,"temp","c")
            self.client.virtualWrite(16,self.startLevel,"batt","p")
            self.client.virtualWrite(9,energyConsumption,"energy","kwh/100km")
            self.client.virtualWrite(10,power,"pow","W")
            self.client.virtualWrite(7, speed,"analog_sensor","null")
            self.client.virtualWrite(8, tempOut,"temp","c")
            self.client.virtualWrite(11, pressure,"analog_sensor","null")
            dataList.insert(8, round(energyConsumption,4))
            dataList.insert(9, round(power,4))
            dataList.insert(10, round(self.startLevel,2))

            self.message =  "{},{},{},{},{},{},{},{},{},{},{}".format(dataList[0],dataList[1],dataList[2],dataList[3], dataList[4], dataList[5], dataList[6],dataList[7],dataList[8],dataList[9],dataList[10])
            
  
    def batteryEnergy(self, startingEnergy, energyIns):
        startingEnergy  =   startingEnergy - energyIns
        return startingEnergy
    
    def energyConsumption(self, power, speed):
        #Power is in [kW] and Speed in [km/h]
        if float(speed) == 0:
            enrgyCon100kmMomentan = 0
        else:
            power = power/1000 #kW
            speedKmh = float(speed) * (3600 / 1000)
            enrgyCon100kmMomentan = (power/speedKmh)*100
        return enrgyCon100kmMomentan
    
    def energyIns(self, power):
        #Power is in [kW] and Speed in [km/h]
        if power == 0:
            energyPortion = 0
        else:
            energyPortion = power/(1000*3600)
        return energyPortion 
    
    def power(self, speed, speed0, alt, alt0, tempOut, pressure, mode, airCondition, tempIn, cAC, desTemp):

        R = 287.05 #gas constant (J/kg.K)
        Af = 2.8 #vehicle frontal area (m^2)
        Cd = 0.29 #aerodynamic drag coefficient
        M = 1345 #mass of vehicle (kg)
        g = 9.81 #acceleration due to gravity (m/s^2)
        c = 0.02 #rolling resistance coefficient
            
        Pa = float(pressure)/(float(tempOut)+273 * R) #air density formula

        if (airCondition == 0) or (mode == '3'):
            Pcc = 0
            if alt0 == 0:
                alt0 = alt
                    
        elif airCondition == 1:
            if float(tempOut) >= tempIn: #AC ON
                if(desTemp == tempIn):
                    Pcc = (cAC[0]*(float(tempOut))+cAC[1])/1000
                else:
                    self.desTemp = tempIn
                    
                    #make matrix for AC
                    AC1 = np.array([[tempIn, 1],[40, 1]])
                    AC2 = np.array([0,5000])
                    #inverse matrix
                    iAC1 = np.linalg.inv(AC1)

                    cAC = np.dot(iAC1,AC2)
                    self.cAC = cAC

                    Pcc = (cAC[0]*(float(tempOut))+cAC[1])/1000

                #print('AC ON')

            elif float(tempOut) < tempIn: #HEATER ON
                if(desTemp == tempIn):
                    Pcc = (cAC[0]*(float(tempOut))+cAC[1])/1000
                else:
                    self.desTemp = tempIn

                    #make matrix for Heater
                    AC1 = np.array([[-5, 1],[tempIn, 1]])
                    AC2 = np.array([5000,0])
                    
                    #inverse matrix
                    iAC1 = np.linalg.inv(AC1)

                    cAC = np.dot(iAC1,AC2)
                    self.cAC = cAC
                    Pcc = ((cAC[0]*float(tempOut))+cAC[1])/1000
#                 print('HEATER ON')
                
        if alt0 == 0:
            alt0 = alt
                
        Wb = 0.5*M*((float(speed)*float(speed))-(float(speed0)*float(speed0))) 
        Wh = M*g*(float(alt)-float(alt0))  
        Wr = (M*g*c +  0.5*Pa*Af*Cd*float(speed)*float(speed))*(0.5*(float(speed)+float(speed0))*1) #t=1s   
#         print('KE:',Wb,'PE:',Wh,'Resistance:',Wr)
        powerOut = (Wb+Wh+Wr) + Pcc # in 1 second
        self.speed0=speed
        self.alt0=alt
        
        #Power saving mode
        if mode == '3': #ECO PRO +
            powerOut = 0.8*powerOut
        elif mode == '2':#ECO PRO
            powerOut = 0.9*powerOut
        else:
            pass

        return powerOut
    
    def setStop(self):
        self.stop = False

    def setStart(self):
        self.stop = True

    def setExit(self):
        self.exit = False
    
    def getMessageServer(self):
        return self.messageServer
    
    def getFeedback(self):
        return self.feedback
    
    def setData(self, data):
        self.message = data
    
    def getData(self):    
        return self.message
    
    def setIP(self, host):
        self.host = host

    def __exit__(self):
        self.messageServer = "NO SERVER CONNECTED!"