# -*- coding: utf-8 -*-
#!/usr/bin/python3
import tkinter
from tkinter import *
from datetime import *
from connections import internetConnection
from datacollector import gpsModul
from datacollector import temperatureSensor
from datacollector import weatherServer
import parameter
import time
import numpy as np
from tkinter import messagebox


#no need to self the pages
class Gui(Canvas):
    
    desTemp = 0 #intilize desired temperature

    def __init__(self):
        self.cloudConnection = internetConnection.CloudConnection()
        self.weather = weatherServer.Weather(self.cloudConnection)
        self.temperatureInside = temperatureSensor.TemperatureSensor(self.cloudConnection)        
        self.gpsData = gpsModul.GpsModul(self.cloudConnection)

        main = tkinter.Tk()
        main.title("E-Car Energy Consumption Tracker")
        main.geometry('800x480')
        main.attributes('-fullscreen', True)
        main.configure(bg='white')
        main.config(cursor='coffee_mug red white')
         
        #Bilder erzeugen
        global pic_option, pic_hska, pic_ump , pic_power, pic_start, pic_cover, pic_submit
        pic_option=PhotoImage(file='/home/pi/Desktop/EtaNetPythonClients-GPSeTracker/images/pic_option.png')
        pic_start=PhotoImage(file='/home/pi/Desktop/EtaNetPythonClients-GPSeTracker/images/pic_start.png')
        pic_submit=PhotoImage(file='/home/pi/Desktop/EtaNetPythonClients-GPSeTracker/images/pic_submit.png')
        pic_cover=PhotoImage(file='/home/pi/Desktop/EtaNetPythonClients-GPSeTracker/images/pic_cover.png')
        pic_hska=PhotoImage(file='/home/pi/Desktop/EtaNetPythonClients-GPSeTracker/images/pic_hska.png')
        pic_power=PhotoImage(file='/home/pi/Desktop/EtaNetPythonClients-GPSeTracker/images/pic_power.png')
        pic_ump=PhotoImage(file='/home/pi/Desktop/EtaNetPythonClients-GPSeTracker/images/pic_ump.png')
        
        #Main Background
        background_main=Canvas(main, width='810', height='40', bd=0, bg='white', highlightthickness=0)
        background_main.create_line(0,36, 810, 36, fill='#f00000', width='2')
        background_main.place(x=-5, y=-5)
        timelbl=Label(main, fg='magenta4', bg='white', font='Roboto')
        timelbl.place(x=10,y=6)
        self.timeLabel = timelbl
        
        
        #Erzeugen der Frames
        self.page_1_1=Frame(main, width=800, height=448, bg='white')
        self.page_1_2=Frame(main, width=800, height=448, bg='white')
        self.page_1_3=Frame(main, width=800, height=448, bg='red')
        self.page_1_4=Frame(main, width=800, height=448, bg='red')
        self.page_1_1.place(x=0, y=33)
        
        #Seite 1.1: Geometrie
        background_p1=Canvas(self.page_1_1, width='780', height='455', bd=0, bg='white', highlightthickness=0)
        background_p1.place(x=0,y=0)
        background_p1.create_image(50,17, image=pic_ump , anchor=NW)
        background_p1.create_image(580,25, image=pic_hska , anchor=NW)
        
        #Seite 1.1: Buttons
        button_start=Button(self.page_1_1, bd=0, fg='black', bg='white', highlightbackground='white', image = pic_start, command = self.switch_page_1_2)
        button_start.place(x=330,y=370)
        button_exit=Button(self.page_1_1, bd=0, fg='black', bg='white', highlightbackground='white', image= pic_power, command = main.destroy)
        button_exit.place(x=705,y=360)
        
        #Seite 1.1: Titel
        titel_1=Label(self.page_1_1, image = pic_cover, bd=0, fg='black', bg='white', highlightbackground='white')
        titel_1.place(x=410, y=80)
        titel_2=Label(self.page_1_1, text='E-Car', fg='red4', bg='white', font= ('Arial',42))
        titel_2.place(x=140, y=95)
        titel_3=Label(self.page_1_1, text='Energy', fg='red4', bg='white', font= ('Arial',42))
        titel_3.place(x=125, y=155)
        titel_4=Label(self.page_1_1, text='Consumption', fg='red4', bg='white', font= ('Arial',42))
        titel_4.place(x=50, y=220)
        titel_5=Label(self.page_1_1, text='Tracker', fg='red4', bg='white', font= ('Arial',42))
        titel_5.place(x=120, y=285)
        
        
        #Seite 1.2: Geometrie
        background_p2=Canvas(self.page_1_2, width='700', height='455', bd=0, bg='white', highlightthickness=0)
        background_p2.place(x=0,y=0)

        #Seite 1.2: Buttons
        button_submit=Button(self.page_1_2, bd=0, fg='black', bg='white',highlightbackground='white', image= pic_submit, state = DISABLED, command = self.switch_page_1_3) #self.answer 
        button_submit.place(x=330,y=370)
        button_exit=Button(self.page_1_2, bd=0, fg='black', bg='white',highlightbackground='white', image= pic_power, command = main.destroy)
        button_exit.place(x=705,y=360)
        self.button_submit=button_submit
        
        #Seite 1.2
        slider = IntVar()
        title_p2=Label(self.page_1_2, text= 'Vehicle Configuration', fg='magenta4', bg='white', font=('Arial',18, 'underline','bold'))
        title_p2.place(x=280, y=5)
        
        #Seite 1.2 Akkulevel
        opt_b1=Label(self.page_1_2, text='Battery level (%) : ', fg='deeppink4', bg='white', font=('Arial',18))
        opt_b1.place(x=20, y=60)
        self.battery_lvl = IntVar() #variable = self.battery_lvl
        opt_b2=Scale(self.page_1_2, from_=0, to_=100, length=440, variable = self.battery_lvl,orient=HORIZONTAL, width=50 , bg = 'peachpuff',sliderlength = 70, font=('Arial',15),command=self.print_batteryLevel)
        opt_b2.place(x=250, y=50)
        opt_b2.set(50)
      
        #Seite 1.2 Climate Control
        self.climate_control= StringVar()
        self.climate_control.trace("w", self.myfunction)
        opt_cc1=Label(self.page_1_2, text='Climate control :', fg='deeppink4', bg='white' , font=('Arial',18))
        opt_cc1.place(x=35, y=150)
        opt_cc2=Radiobutton(self.page_1_2, fg='black', bg='peachpuff' , font=('Arial',25), width= 8,text= 'On', variable = self.climate_control , value = '1', indicatoron=0, command=self.print_climateControl)
        opt_cc2.place(x=270, y=150)
        opt_cc3=Radiobutton(self.page_1_2, fg='black', bg='peachpuff' , font=('Arial',25), width= 8, text= 'Off', variable = self.climate_control , value = '0', indicatoron=0, command= self.print_climateControl)
        opt_cc3.place(x=530, y=150)
        
        #Seite 1.2 Temp in
        opt_b3=Label(self.page_1_2, text='Car Temperature : ', fg='deeppink4', bg='white', font=('Arial',18))
        opt_b3.place(x=10, y=240)
        self.desired_temp= IntVar()
        opt_b4=Scale(self.page_1_2, from_=10, to_=30, length=440, orient=HORIZONTAL, variable = self.desired_temp,width=50 , bg = 'peachpuff',sliderlength = 70, font=('Arial',15),command=self.print_desiredTemp)
        opt_b4.place(x=250, y=220)
        opt_b4.set(24)
            
        #Seite 1.2 Driving Mode
        self.driving_mode = StringVar()
        self.driving_mode.trace("w", self.myfunction)
        opt_dm1=Label(self.page_1_2, text='Driving mode : ', fg='deeppink4', bg='white', font=('Arial',18))
        opt_dm1.place(x=55, y=320)
        opt_dm2=Radiobutton(self.page_1_2, fg='black', bg='peachpuff' , font=('Arial',25), width= 8, text= 'Comfort', variable = self.driving_mode , value = '0',indicatoron=0, command=self.print_drivingmode)
        opt_dm2.place(x=250, y=320)
        opt_dm3=Radiobutton(self.page_1_2, fg='black', bg='peachpuff', font=('Arial',25), width= 8, text= 'Eco Pro', variable = self.driving_mode , value = '1',indicatoron=0, command=self.print_drivingmode)
        opt_dm3.place(x=420, y=320)
        opt_dm4=Radiobutton(self.page_1_2, fg='black', bg='peachpuff' , font=('Arial',25), width= 8, text= 'Eco Pro+', variable = self.driving_mode , value = '2',indicatoron=0, command=self.print_drivingmode)
        opt_dm4.place(x=590, y=320)
        
        
        #Seite 1.3: Geometrie
        background_opt3=Canvas(self.page_1_3, width='700', height='455', bd=0, bg='white', highlightthickness=0)
        background_opt3.place(x=0,y=0)
        background_opt31=Canvas(self.page_1_3, width='300', height='180', bd=0, bg='lightpink', highlightthickness=0)
        background_opt31.place(x=20,y=50)
        background_opt32=Canvas(self.page_1_3, width='320', height='110', bd=0, bg='lightpink', highlightthickness=0)
        background_opt32.place(x=360,y=50)
        background_opt33=Canvas(self.page_1_3, width='300', height='180', bd=0, bg='lightpink', highlightthickness=0)
        background_opt33.place(x=20,y=245)
        background_opt34=Canvas(self.page_1_3, width='320', height='110', bd=0, bg='lightpink', highlightthickness=0)
        background_opt34.place(x=360,y=315)
        background_opt35=Canvas(self.page_1_3, width='320', height='110', bd=0, bg='lightpink', highlightthickness=0)
        background_opt35.place(x=360,y=185)        
        
        #Seite 1.3: Buttons
        button_setting=Button(self.page_1_3, image = pic_option, bd=0, highlightthickness=0,highlightcolor = 'red', bg = 'red',command=self.switch_page_1_2) #text = 'Settings'
        button_setting.place(x=700,y=140)
        button_exit=Button(self.page_1_3, bd=0, highlightthickness=0,highlightcolor = 'red', bg = 'red', image= pic_power, command= main.destroy)
        button_exit.place(x=710,y=320)

        #Seite 1.3: Höheneinstellungen 
        opt_title_1=Label(self.page_1_3, text='Output data', fg='magenta4', bg='white', font=('Arial',18,'underline','bold'))
        opt_title_1.place(x=300, y=5)
        
        #GPS
        opt_gps1=Label(self.page_1_3, text= 'GPS Data', fg='black', bg='lightpink', font=('Arial',15,'bold','underline'))
        opt_gps1.place(x=468, y=50)   
        opt_gps2=Label(self.page_1_3, text= ' Latitude: ', fg='black', bg='lightpink', font=('Arial',14,'bold'))
        opt_gps2.place(x=360, y=80)
        self.opt_gps2_val=Label(self.page_1_3, text= 'value',width = 13,anchor = 'e', fg='black', bg='lightpink', font=('Arial',13))
        self.opt_gps2_val.place(x=500, y=82)

        opt_gps3=Label(self.page_1_3, text= ' Longitude: ', fg='black', bg='lightpink', font=('Arial',14,'bold'))
        opt_gps3.place(x=360, y=105)
        self.opt_gps3_val=Label(self.page_1_3, text= 'value',width = 13,anchor = 'e', fg='black', bg='lightpink', font=('Arial',13))
        self.opt_gps3_val.place(x=500, y=105)
        
        opt_gps4=Label(self.page_1_3, text=' Speed : ', fg='black', bg='lightpink', font=('Arial',14,'bold'))
        opt_gps4.place(x=360, y=130)
        self.opt_gps4_val=Label(self.page_1_3, text='value',width = 15,anchor = 'e', fg='black', bg='lightpink', font=('Arial',13))
        self.opt_gps4_val.place(x=480, y=130)
        
        #Car Configuration
        opt_car1=Label(self.page_1_3, text='Car Settings ', fg='black', bg='lightpink', font=('Arial',15,'bold','underline'))
        opt_car1.place(x=110, y=60)
        
        opt_car2=Label(self.page_1_3, text=' Desired Temperature:', fg='black', bg='lightpink', font=('Arial',14,'bold'))
        opt_car2.place(x=20, y=90)
        self.opt_car2_val=Label(self.page_1_3, text='value', width = 8,anchor = 'e',fg='black', bg='lightpink', font=('Arial',13))
        self.opt_car2_val.place(x=220, y=91)
        
        opt_car3=Label(self.page_1_3, text=' Driving Mode:', fg='black', bg='lightpink', font=('Arial',14,'bold'))
        opt_car3.place(x=20, y=120)
        self.opt_car3_val=Label(self.page_1_3, text='value',width = 14,anchor = 'e', fg='black', bg='lightpink', font=('Arial',13))
        self.opt_car3_val.place(x=160, y=121)
        
        opt_car4=Label(self.page_1_3, text=' Climate control :', fg='black', bg='lightpink', font=('Arial',14,'bold'))
        opt_car4.place(x=20, y=150)
        self.opt_car4_val=Label(self.page_1_3, text= 'value',width = 12,anchor = 'e', fg='black', bg='lightpink', font=('Arial',13))
        self.opt_car4_val.place(x=180, y=151)
        
        opt_car6=Label(self.page_1_3, text=' Indoor Temperature :', fg='black', bg='lightpink', font=('Arial',14,'bold'))
        opt_car6.place(x=20, y=180)
        self.opt_car6_val=Label(self.page_1_3, text= 'value', fg='black', bg='lightpink', font=('Arial',13))
        self.opt_car6_val.place(x=220, y=180)
        
        opt_e1=Label(self.page_1_3, text=' Energy ', fg='black', bg='lightpink', font=('Arial',15,'bold','underline'))
        opt_e1.place(x=480, y=188)
        
        opt_car5=Label(self.page_1_3, text=' Battery level :', fg='black', bg='lightpink', font=('Arial',14,'bold'))
        opt_car5.place(x=360, y=216)
        self.opt_car5_val=Label(self.page_1_3, text='value', width = 12,anchor = 'e',fg='black', bg='lightpink', font=('Arial',13))
        self.opt_car5_val.place(x=505, y=218)
        
        opt_e2=Label(self.page_1_3, text='Power :', fg='black', bg='lightpink', font=('Arial',14,'bold'))
        opt_e2.place(x=365, y=240)
        self.opt_e2_val=Label(self.page_1_3, text='value', width = 12,anchor = 'e',fg='black', bg='lightpink', font=('Arial',13))
        self.opt_e2_val.place(x=505, y=242)
        
        opt_e3=Label(self.page_1_3, text='Energy/100km :', fg='black', bg='lightpink', font=('Arial',14,'bold'))
        opt_e3.place(x=365, y=265)
        self.opt_e3_val=Label(self.page_1_3, text='value',width = 13,anchor = 'e', fg='black', bg='lightpink', font=('Arial',12))
        self.opt_e3_val.place(x=505, y=267)
        
        #Weather
        opt_w1=Label(self.page_1_3, text=' Weather API ', fg='black', bg='lightpink', font=('Arial',15,'bold','underline'))
        opt_w1.place(x=100, y=250)
        
        opt_w2=Label(self.page_1_3, text=' Outdoor Temperature:', fg='black', bg='lightpink', font=('Arial',14,'bold'))
        opt_w2.place(x=20, y=280)
        self.opt_w2_val=Label(self.page_1_3, text='value',width = 8,anchor = 'e', fg='black', bg='lightpink', font=('Arial',13))
        self.opt_w2_val.place(x=220, y=282)
        
        opt_w3=Label(self.page_1_3, text=' Weather description : ', fg='black', bg='lightpink', font=('Arial',14,'bold'))
        opt_w3.place(x=20, y=315)
        self.opt_w3_val=Label(self.page_1_3, text='value',width = 19,anchor = 'e', fg='black', bg='lightpink', font=('Arial',14))
        self.opt_w3_val.place(x=90, y=347)
        
        opt_w4=Label(self.page_1_3, text=' Outdoor Pressure:', fg='black', bg='lightpink', font=('Arial',14,'bold'))
        opt_w4.place(x=20, y=380)
        self.opt_w4_val=Label(self.page_1_3, text='value',width = 11,anchor = 'e', fg='black', bg='lightpink', font=('Arial',13))
        self.opt_w4_val.place(x=190, y=381)
        
        #Cloud Connection
        opt_c1=Label(self.page_1_3, text=' Cloud Connection', fg='black', bg='lightpink', font=('Arial',15,'bold','underline'))
        opt_c1.place(x=430, y=317)
        opt_c2=Label(self.page_1_3, text=' IP :', fg='black', bg='lightpink', font=('Arial',14,'bold'))
        opt_c2.place(x=360, y=347)
        opt_c2=Label(self.page_1_3, text=' 192.168.1.104 ', fg='black', bg='lightpink', font=('Arial',13))
        opt_c2.place(x=500, y=347)
        
        opt_c3=Label(self.page_1_3, text=' Port :', fg='black', bg='lightpink', font=('Arial',14,'bold'))
        opt_c3.place(x=360, y=367)
        opt_c3=Label(self.page_1_3, text=' 1883 ', fg='black', bg='lightpink', font=('Arial',13))
        opt_c3.place(x=500, y=367)
        
        opt_c4=Label(self.page_1_3, text=' Cloud name :', fg='black', bg='lightpink', font=('Arial',14,'bold'))
        opt_c4.place(x=360, y=388)
        opt_c4=Label(self.page_1_3, text=' Cayenne IoT', fg='black', bg='lightpink', font=('Arial',13))
        opt_c4.place(x=500, y=388)
        
        Frame.__init__(self, main)

        
    def connect(self):
        ipAddr = self.entry.get()
        try:
            pass
        except:
            if parameter.printMessages:
                print ("Please switch on the Server-App!")
            self.messageServer = "NO SERVER CONNECTED!"
            print("NO SERVER CONNECTED!")

    def stopMeasure(self):
        self.weather.setStop()
        self.temperatureInside.setStop()
        self.gpsData.setStop()
        
    def startMeasure(self):
        self.weather.setStart()
        self.temperatureInside.setStart()
        self.gpsData.setStart()
        
    def __exit__(self):
        self.temperatureInside.setExit()
        self.temperatureInside.__exit__()
        self.weather.setExit()
        self.gpsData.setExit()
        self.cloudConnection.setExit()
        self.cloudConnection.__exit__()
    
    def exitApp(self):
        self.page_1_1.destroy()
        self.page_1_2.destroy()
        self.page_1_3.destroy()
        self.page_1_4.destroy()
    
    def print_climateControl(self):
        cc = self.climate_control.get()
        if cc == '1':
            self.opt_car4_val['text'] = 'ON'
            ccInt = 1
        elif cc =='0':
            self.opt_car4_val['text'] = 'OFF'
            ccInt = 0
            self.cloudConnection.setAirCondition(ccInt)
        return cc

    def print_drivingmode(self):
        dm = self.driving_mode.get()
        self.cloudConnection.setCarMode(dm)
        if dm == '0':
            self.opt_car3_val['text'] = 'Comfort mode'
        elif dm == '1':
            self.opt_car3_val['text'] = 'Eco Pro Mode'
        elif dm == '2':
            self.opt_car3_val['text'] = 'Eco Pro+ Mode'
        return dm
    
    def print_batteryLevel(self,battLvl):
        battLvl = self.battery_lvl.get()
        batterieLvl=self.cloudConnection.setStartLevelBattery(battLvl)
        self.opt_car5_val['text'] = (batterieLvl,'%')   
        
    def print_desiredTemp(self, dTemp):
        dTemp = self.desired_temp.get()
        self.cloudConnection.setTempIn(dTemp)
        self.opt_car2_val['text'] = (dTemp,'°C')

    def myfunction(self,*args):
        x = self.climate_control.get()
        y = self.driving_mode.get()
        if x and y:
            self.button_submit.config(state='normal')
        else:
           self.button_submit.config(state='disabled')

    def visualizationData(self):
        data = self.cloudConnection.getData()
        dataList = data.split(',')
        try:
            self.opt_car5_val['text'] = dataList[10]+'%' #batterylvl UNCOMMENT
            self.opt_e2_val['text'] = dataList[9]+'W'#power
            self.opt_e3_val['text'] = dataList[8]+'kWh/100km'#kwh/100km
        except IndexError:
            pass
        finally:
            self.opt_gps2_val['text'] = dataList[5]+'°' #lat val
            self.opt_gps3_val['text'] = dataList[4]+'°' #lon val
            self.opt_gps4_val['text'] = dataList[6]+'km/h' #speed
            self.opt_car6_val['text'] = dataList[3]+'°C' #indoor temp
            self.opt_w2_val['text'] = dataList[0]+'°C' #tOut
            self.opt_w3_val['text'] = dataList[2] #weatherDesc
            self.opt_w4_val['text'] = dataList[1]+'kPa' #pressure
            self.print_climateControl()
            self.print_drivingmode()
            self.after(parameter.timeTriggervisualData, self.visualizationData)
        
    def switch_page_1_1(self):
        self.page_1_1.place(x=0, y=33)
        self.page_1_2.place_forget()
        self.page_1_3.place_forget()
        self.page_1_4.place_forget()
        
    def switch_page_1_2(self):
        self.page_1_1.place_forget()
        self.page_1_2.place(x=0, y=33)
        self.page_1_3.place_forget()
        self.page_1_4.place_forget()
        
    def switch_page_1_3(self):
        self.page_1_1.place_forget()
        self.page_1_2.place_forget()
        self.page_1_3.place(x=0, y=33)
        self.page_1_4.place_forget()
        
    def switch_page_1_4(self):
        self.page_1_1.place_forget()
        self.page_1_2.place_forget()
        self.page_1_3.place_forget()
        self.page_1_4.place(x=0, y=33)

    # lokale Zeit:
    def localtime(self):
        self.timeLabel.configure(text=datetime.today().strftime("%d.%m.%Y %H:%M:%S"))
        self.timeLabel.after(1000, self.localtime)
