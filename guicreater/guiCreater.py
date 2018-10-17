
from tkinter import *
from connections import networkConnection as etaNet
from datacollector import powerAnalyzer
from datacollector import gasMassFlow
from datacollector import heatMeter
from controlling import relaisRemoteSwitches
import parameter
import time

class Gui(Frame):
    # Members
    textPower = 'Hallo IKKUengine!'
    textSignal = 'Hallo IKKUengine!'

    def __init__(self):
        self.netConn = etaNet.etaNetClient()
        self.powerAn = powerAnalyzer.PowerAnalyzer(self.netConn)
        self.massFlow = gasMassFlow.MassFlow(self.netConn)
        self.relais = relaisRemoteSwitches.RemoteSwitches(self.netConn)
        self.heatMeater1 = heatMeter.HeatMeter(self.netConn, 1)
        time.sleep(1)
        self.heatMeater2 = heatMeter.HeatMeter(self.netConn, 2)
        # subject.notify_observers('done')
        # GUI Init
        # self.requestPowerAnalyzer()
        master = Tk()
        menu_bar = Menu(master)
        self.infoText = Label(master, text=self.textPower, fg="red")
        self.infoText.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.signalText = Label(master, text=self.textSignal, bg="yellow")
        self.signalText.place(relx=0.99, rely=0.001, anchor=NE)
 
        main_menu = Menu(menu_bar, tearoff=0)
        measure_menu = Menu(menu_bar, tearoff=0)
        controlling_menu = Menu(menu_bar, tearoff=0)
        measure_menu.add_command(label="Stop Measure", command=self.stopMeasure)
        measure_menu.add_command(label="Start Measure", command=self.startMeasure)
        measure_menu.add_command(label="Stop Transfer", command=self.netConn.setStop)
        measure_menu.add_command(label="Start Transfer", command=self.netConn.setStart)
        controlling_menu.add_command(label="On/Off CHP", command=self.relais.setRelaisCHPOnOff)
        main_menu.add_command(label="Quit", command=master.destroy)

        menu_bar.add_cascade(label="Menu", menu=main_menu)
        menu_bar.add_cascade(label="Measurement", menu=measure_menu)
        menu_bar.add_cascade(label="Controlling", menu=controlling_menu)
        master.config(menu=menu_bar)
        if parameter.fullscreen:
            master.attributes('-fullscreen', True)
        Frame.__init__(self, master)

    def stopMeasure(self):
        self.powerAn.setStop()
        self.massFlow.setStop()
        self.heatMeater1.setStop()
        self.heatMeater2.setStop()
        self.relais.setStop()
        
    def startMeasure(self):
        self.powerAn.setStart()
        self.massFlow.setStart()
        self.heatMeater1.setStart()
        self.heatMeater2.setStart()
        self.relais.setStart()
        
    def __exit__(self):
        self.powerAn.setExit()
        self.powerAn.__exit__()
        self.massFlow.setExit()
        self.heatMeater1.setExit()
        self.heatMeater1.__exit__()
        self.heatMeater2.setExit()
        self.heatMeater2.__exit__()
        self.relais.setExit()
        self.netConn.setExit()
        self.netConn.__exit__()
        
    def visualizationData(self):
        self.infoText['text'] = self.adaptDataList()
        self.signalText['text'] = self.netConn.getMessageServer()
        self.after(parameter.timeTriggervisualData, self.visualizationData)
        
    def adaptDataList(self):
        adaptData = "{}\n\r{}\n\r{}\n\r{}\n\r{}".format(self.powerAn.getData(), self.heatMeater1.getData(), \
                    self.heatMeater2.getData(), self.massFlow.getData(), self.relais.getData())
        return adaptData
