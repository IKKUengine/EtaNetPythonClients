import time
import serial
from threading import Thread
from tkinter import *
import RPi.GPIO as GPIO
import Adafruit_ADS1x15



#ToDo: Überblicksdokumentation
#why threading? -> if one of the requests in work and cannot continue
#than the system will not blocked


class guiApplication(Frame):

    #Members
    textPower = 'Hallo IKKUengine!'
    textSignal = ''
    
    # Choose a gain of 1 for reading voltages from 0 to 4.09V.
    # Or pick a different gain to change the range of voltages that are read:
    #  - 2/3 = +/-6.144V
    #  -   1 = +/-4.096V
    #  -   2 = +/-2.048V
    #  -   4 = +/-1.024V
    #  -   8 = +/-0.512V
    #  -  16 = +/-0.256V
    # See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
    GAIN = 1
        
    

    ser = serial.Serial (
        port='/dev/ttyS0', #Open RPI buit-in serial port
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
      
    def __init__(self, master=None):
        
        #Hardware Init
        
        # Create an ADS1115 ADC (16-bit) instance.
        self.adc = Adafruit_ADS1x15.ADS1115()

        # Note you can change the I2C address from its default (0x48), and/or the I2C
        # bus by passing in these optional parameters:
        #adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(12, GPIO.OUT)
        
        if GPIO.input(12):
            self.textSignal = 'CHP is ON at Start'
        else:
            self.textSignal = 'CHP is OFF at Start' 
              
        #GUI Init
        #self.requestPowerAnalyzer()
        self.infoText= Label(master, text=self.textPower, fg="red")
        self.infoText.place(relx=0.5, rely = 0.5, anchor= CENTER)
        self.signalText = Label(master, text=self.textSignal, bg="yellow")
        self.signalText.place(relx=0.99, rely = 0.001, anchor= NE)
        Button(master, text = 'Messen', width=20, command = self.requestPowerAnalyzer).place(relx=0.8, rely = 0.98, anchor= SE)
        Button(master, text = 'Schließen', width=20, command = root.destroy).place(relx=0.98, rely = 0.98, anchor= SE) 
        
        Frame.__init__(self, master)

        
    def __exit__(self, master):
         GPIO.cleanup()

    
    def requestPowerAnalyzer(self):
    
        #t=Thread(target=self.masurementRunning, args=()).start()
        #self.ser.write(str.encode('FORM:PH L1\n'))
        #self.ser.write(str.encode('VOLT:RMS:AC?\n'))
        #ser.write(str.encode('CURR:RMS:AC?\n'))
        #ser.write(str.encode('POW:FAC:AC?\n'))       
        #data1 = self.ser.read(10) #Read 10 characters from serial port to data
        self.ser.write(str.encode('POW:ACT:AC?\n'))
        #data2 = self.ser.read(15)

        #ser.write(str.encode('POW:ACT:AC? FORM:PH L1?\n'))
        #data3 = ser.read(40)

        #ser.write(str.encode('POW:ACT:AC? FORM:PH L2?\n'))
        #data4 = ser.read(40)

        #ser.write(str.encode('POW:ACT:AC? FORM:PH L3?\n'))
        #data5 = ser.read(40)

        #self.ser.write(str.encode('FORM:PH L3\n'))

        self.ser.write(str.encode('VOLT:RMS:AC?\n'))
        #ser.write(str.encode('CURR:RMS:AC?\n'))
        #ser.write(str.encode('POW:FAC:AC?\n'))       
        data = self.ser.read(22) #Read 10 characters from serial port to data

        #self.ser.write(str.encode('POW:ACT:AC?\n'))
        #data5 = self.ser.read(10)

        #ser.write(str.encode('POW:ACT:AC? FORM:PH L1?\n'))
        #data3 = ser.read(40)

        #ser.write(str.encode('POW:ACT:AC? FORM:PH L2?\n'))
        #data4 = ser.read(40)
        
        #ser.write(str.encode('POW:ACT:AC? FORM:PH L3?\n'))
        #data5 = ser.read(40)

        #ser.write(str.encode('FORM:PH L3\n'))
        #data6 = ser.read(100)

        #ser.write(str.encode('POW:ACT:AC?\n'))
        #data3 = ser.read(100)

        self.infoText['text'] =  data

        self.ser.close
    
    def requestGasMassFlow(self):
        # Read all the ADC channel values in a list.
        values = [0]*4
        #for i in range(4):
        # Read the specified ADC channel using the previously set gain value.
        values[0] = self.adc.read_adc(0, gain=self.GAIN)
        #values[1] = adc.read_adc(1, gain=GAIN)
        #values[2] = adc.read_adc(2, gain=GAIN)
        #values[3] = adc.read_adc(3, gain=GAIN)
        # Note you can also pass in an optional data_rate parameter that controls
        # the ADC conversion time (in samples/second). Each chip has a different
        # set of allowed data rate values, see datasheet Table 9 config register
        # DR bit values.
        #values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
        # Each value will be a 16 bit signed integer value depending on the
        # ADC (ADS1115 = 16-bit).
        
        #Calculation and calibration of the gas fuel flow
        fuelflow = (values[0]) / (2 * 3276.8) * 4.2 * 0.046166667
        self.infoText['text'] = str(fuelflow)

    def requestHeatMeterHotWater(self):
        self.infoText['text'] = 'Heat Meter 2 (Warmwasser) muss noch implementiert werden...'

    def requestHeatMeterHeatingWater(self):
        self.infoText['text'] = 'Heat Meter 1 (Heizwasser) muss noch implementiert werden...'

    def requestTimeDate(self):
        self.infoText['text'] = 'Time/Date muss noch implementiert werden...'

    def setOnOffCHP(self):
        if GPIO.input(12):
            self.signalText['text'] = 'CHP is OFF'
        else:
            self.signalText['text'] = 'CHP is ON'
        GPIO.output(12, not GPIO.input(12)) 

    def requestWeatherData(self):
        self.infoText['text'] = 'Weather Data muss noch implementiert werden...'

    
    def saveData(self):
        self.infoText['text'] = 'Save Data muss noch implementiert werden...'
        
    def masurementRunning(self):
        self.infoText['text'] = 'Die Messung läuft! Bitte warten...'

root = Tk()
menu_bar = Menu(root)
window = guiApplication(master = root)
main_menu = Menu(menu_bar, tearoff=0)
measure_menu = Menu(menu_bar, tearoff=0)
controlling_menu = Menu(menu_bar, tearoff=0)
measure_menu.add_command(label="Power Analyzer", command=window.requestPowerAnalyzer)
measure_menu.add_command(label="Gas Mass Flow", command=window.requestGasMassFlow)
measure_menu.add_command(label="Heat Meter 1", command=window.requestHeatMeterHeatingWater)
measure_menu.add_command(label="Heat Meter 2", command=window.requestHeatMeterHotWater)
measure_menu.add_command(label="Weather Data", command=window.requestWeatherData)
measure_menu.add_command(label="Time/Date", command=window.requestTimeDate)
controlling_menu.add_command(label="On/Off CHP", command=window.setOnOffCHP)
main_menu.add_command(label="Save Data", command=window.saveData)
main_menu.add_command(label="Quit", command=root.destroy)

menu_bar.add_cascade(label="Menu", menu = main_menu)
menu_bar.add_cascade(label="Single Measurement", menu = measure_menu)
menu_bar.add_cascade(label="Controlling", menu = controlling_menu)

root.config(menu=menu_bar)
root.attributes('-fullscreen',True)
window.mainloop()




#for i in range(10):
#    t = Thread(target=sleeper, args=(i,))
#    t.start()