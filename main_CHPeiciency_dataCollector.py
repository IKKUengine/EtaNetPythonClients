import time
import serial
from threading import Thread
from tkinter import *


#ToDo: Überblicksdokumentation
#why threading? -> if one of the requests in work and cannot continue
#than the system will not blocked


class guiApplication(Frame):

    #Members
    textPower = 'Anwendung wird gestartet...'
    


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
        self.infoText.grid(row = 0)
        Button(master, text = 'Messen', width=20, command = self.requestPowerAnalyzer).grid(row = 1, column = 0)
        Button(master, text = 'Schließen', width=20, command = root.destroy).place(relx=0.98, rely = 0.98, anchor= SE) #grid(row = 1, column = 1)
        
        Frame.__init__(self, master)

        
                
    def requestPowerAnalyzer(self):
    
        self.ser.write(str.encode('FORM:PH L1\n'))
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
    
    def requestGasMassFlow():
        pass

    def requestHeatMeter():
        pass

    def requestTime():
        pass

    def setOnOffBHKW():
        pass

    def requestWeatherData():
        pass



root = Tk()
window = guiApplication(master = root)
root.attributes('-fullscreen',True)
window.mainloop()




#for i in range(10):
#    t = Thread(target=sleeper, args=(i,))
#    t.start()