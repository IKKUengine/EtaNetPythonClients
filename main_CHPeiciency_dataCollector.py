import time
import serial
from threading import Thread
from tkinter import *


#ToDo: Überblicksdokumentation
#why threading? -> if one of the requests in work and cannot continue
#than the system will not blocked


class guiApplication(Frame):

    #Members
    textPower = 'Hallo IKKUengine!'
    


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

              
        #GUI Init
        #self.requestPowerAnalyzer()
        self.infoText= Label(master, text=self.textPower, fg="red")
        self.infoText.place(relx=0.5, rely = 0.5, anchor= CENTER)
        Button(master, text = 'Messen', width=20, command = self.requestPowerAnalyzer).place(relx=0.8, rely = 0.98, anchor= SE)
        Button(master, text = 'Schließen', width=20, command = root.destroy).place(relx=0.98, rely = 0.98, anchor= SE) 
        
        Frame.__init__(self, master)

        
                
    def requestPowerAnalyzer(self):
    
        #t=Thread(target=self.masurementRunning, args=()).start()
        #self.ser.write(str.encode('FORM:PH L1\n'))
        self.ser.write(str.encode('VOLT:RMS:AC?\n'))
        #ser.write(str.encode('CURR:RMS:AC?\n'))
        #ser.write(str.encode('POW:FAC:AC?\n'))       
        data1 = self.ser.read(40) #Read 10 characters from serial port to data
        self.ser.write(str.encode('POW:ACT:AC?\n'))
        data2 = self.ser.read(40)

        #ser.write(str.encode('POW:ACT:AC? FORM:PH L1?\n'))
        #data3 = ser.read(40)

        #ser.write(str.encode('POW:ACT:AC? FORM:PH L2?\n'))
        #data4 = ser.read(40)

        #ser.write(str.encode('POW:ACT:AC? FORM:PH L3?\n'))
        #data5 = ser.read(40)

        self.ser.write(str.encode('FORM:PH L3\n'))

        self.ser.write(str.encode('VOLT:RMS:AC?\n'))
        #ser.write(str.encode('CURR:RMS:AC?\n'))
        #ser.write(str.encode('POW:FAC:AC?\n'))       
        data4 = self.ser.read(40) #Read 10 characters from serial port to data

        self.ser.write(str.encode('POW:ACT:AC?\n'))
        data5 = self.ser.read(40)

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

        self.infoText['text'] = data1 + str.encode(";") + data2 + str.encode(";") + data4 + str.encode(";") + data5

        self.ser.close
    
    def requestGasMassFlow(self):
        self.infoText['text'] = 'Gas Mass Flow muss noch implementiert werden...'

    def requestHeatMeterHotWater(self):
        self.infoText['text'] = 'Heat Meter 2 (Warmwasser) muss noch implementiert werden...'

    def requestHeatMeterHeatingWater(self):
        self.infoText['text'] = 'Heat Meter 1 (Heizwasser) muss noch implementiert werden...'

    def requestTimeDate(self):
        self.infoText['text'] = 'Time/Date muss noch implementiert werden...'

    def setOnOffCHP(self):
        self.infoText['text'] = 'ON/OFF BHKW muss noch implementiert werden...'


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