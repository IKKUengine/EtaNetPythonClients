import time
import threading
import parameter
import datetime
import json, requests
import cayenne.client #added

from observer import observe

class WeatherServer(threading.Thread):
    exit = True
    stop = True
    
    def __init__(self):

        try:
#             lat=49.020938167
#             lon=8.389365667
#             key = 'd1460eff29e117c1a377c77c7d9071c4'
#             units = 'metric'
#             url = requests.get('http://api.openweathermap.org/data/2.5/weather?lat='+str(lat)+'&lon='+str(lon)+'&units='+units+'&appid='+key)
            
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
     
        
    # set function here, do not forget the self
    def getAPI(self):
        #request from GPS
        lat=49.020938167
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
        Pout = (weather['main']['pressure']*100)
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
    carMode = 0
    startLevel = 0
    airCondition = 0
    
    def __init__(self):

        observe.Observable.__init__(self)
        threading.Thread.__init__(self)
         
        MQTT_USERNAME  = "20892060-92f2-11ea-93bf-d33a96695544"
        MQTT_PASSWORD  = "b64c0d13e163f20801cabdfd935acefc581b897d"
        MQTT_CLIENT_ID = "31a52d60-d7e6-11ea-a67f-15e30d90bbf4"
          
        self.client = cayenne.client.CayenneMQTTClient()
        self.client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)

        threading.Thread.start(self)
        
    def run(self):
        while self.exit:
            if self.stop:
                self.notify_observersMonitoring()
                time.sleep(parameter.timeTriggerSendData)
                self.sendAllData()
       
    def setCarMode(self, mode):
        self.carMode = mode
        
    def setStartLevelBattery(self, startLevel):
        self.startLevel = startLevel
        
    def setAirCondition(self, enable):
        self.airCondition = enable
        
    def sendAllData(self):

        datetimeCloud = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message =  "'{}' ('TimeStamp', {}) VALUES ('{}', {})".format(parameter.systemIdentifier, self.getHeaderList(), datetimeCloud , self.getDataList()) 
            
        #try:
            # you can use "self.host" or "getIP()" here
            #inside "message" you have all information about weather gps and tem sensor
            # it a string
        #print (self.getDataList())
        self.getDataList()
        self.mqttData(self.getDataList())
       
        self.messageServer = "WITH IoT-CLOUD CONNECTED!"
            #print("SERVER CONNECTED!")
        #except:
            #if parameter.printMessages:
            #    print ("Please switch mount USB-Internetstick!")
            #self.messageServer = "NO CLOUD CONNECTED!"
    
    def mqttData(self, dataString):
        self.setCarMode(1)
        self.setStartLevelBattery(50)
        self.setAirCondition(1)
        dataList = dataString.split(',')
        if len(dataList) >= 7:
            tempOut = dataList[0]
            pressure = dataList[1]
            weatherDescription = dataList[2]
            tempIn = dataList[3]
            lon = dataList[4]
            lat = dataList[5]
            speed = dataList[6]
            power = self.power(speed, tempOut, pressure, self.carMode, self.airCondition)
            energyConsumption = self.energyConsumption(power, speed)
            startingEnergy =  (37.9/100)*self.startLevel 
            self.startLevel = (100/37.9) * self.batteryEnergy(startingEnergy, energyConsumption)
            self.client.loop() 
            self.client.virtualWrite(23, lat,"analog_sensor","null")
            self.client.virtualWrite(17, lon,"analog_sensor","null")
            self.client.virtualWrite(5, tempIn,"temp","c")
            self.client.virtualWrite(16,self.startLevel,"batt","p")
            self.client.virtualWrite(9,energyConsumption,"energy","kwh")
            self.client.virtualWrite(10,power,"pow","kw")
            self.client.virtualWrite(7, speed,"analog_sensor","null")
            self.client.virtualWrite(8, tempOut,"temp","c")
            self.client.virtualWrite(11, pressure,"analog_sensor","null")
            #self.client.on_message = on_message

    def batteryEnergy(self, startingEnergy, energyConsumption):
    #def getBatteryConsumption(EnergyConsumption,startBatt,TotalEnergyConsumed, BattUsed):
        print('Battery level decreasing')
        
        startingEnergy  =   startingEnergy - energyConsumption
        
        return startingEnergy
    
    def energyConsumption(self, power, speed):
        #Power is in [kW] and Speed in [km/h]
        if float(speed) > 0:
            speedKmh = float(speed) * (3600 / 1000)
            enrgyCon100kmMomentan = (power/speedKmh)*100
        else:
            enrgyCon100kmMomentan = 0
        return enrgyCon100kmMomentan
    
    def power(self, speed, tempOut, pressure, mode, airCondition):
    #def climateControl(pressure,tempOut,cc, drvMode, V):
        R = 287.05 #gas constant (J/kg.K)
        Af = 2.8 #vehicle frontal area (m^2)
        Cd = 0.29 #aerodynamic drag coefficient
        M = 1345 #mass of vehicle (kg)
        g = 9.81 #acceleration due to gravity (m/s^2)
        c = 0.02 #rolling resistance coefficient
        a = 0 #gradient of the road. in degrees Depends on user input.
            
        Pa = float(pressure)/(float(tempOut)+273 * R) #air density formula
        
        if (airCondition == 2) or (mode == 3):
            powerOut = (float(speed)*((M*g*c)+(1/2*Pa*float(speed)*float(speed)*Af*Cd)))/1000 #+(M*g*math.sin(a))
            Pcc = 0 

        elif airCondition == 1:
            if float(tempOut) > 22: #AC ON
                    Pcc = ((277.78*float(tempOut))-6111.11)/1000
                    print('AC ON')

            elif float(tempOut) < 22: #HEATER ON 
                    Pcc = ((-185.19*float(tempOut))+4074.07)/1000
                    print('HEATER ON')

            powerOut = ((float(speed)*((M*g*c)+(1/2*Pa*float(speed)*float(speed)*Af*Cd)))/1000)+Pcc #+(M*g*math.sin(a))
            
            if mode == 3:
                powerOut = 0.8*powerOut
           
            elif mode == 2:
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
    

    def __exit__(self):
        self.messageServer = "NO SERVER CONNECTED!"