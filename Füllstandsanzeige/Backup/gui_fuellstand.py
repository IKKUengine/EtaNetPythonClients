#### Einbinden der Bibliotheken ####
from datetime import *

import RPi.GPIO as gpio
import multiprocessing

from tkinter import*
import numpy

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#### Variablen ####
# Globale Variablen:
iniv=0
l24h=0
a_time=[0]*10
a_time_l24h=[0]*288
heatlevel=[0]*10
heatlevel_l24h=[0]*288

# Prozessübergreifende Variablen:
t1 =multiprocessing.Value("d",0.0)
t2 =multiprocessing.Value("d",0.0)
t3 =multiprocessing.Value("d",0.0)
t4 =multiprocessing.Value("d",0.0)
t5 =multiprocessing.Value("d",0.0)

# Sensorpfade:
wire1='/sys/devices/w1_bus_master1/3b-2c98073da241/w1_slave'
wire2='/sys/devices/w1_bus_master1/3b-2c98073db8b6/w1_slave'
wire3='/sys/devices/w1_bus_master1/3b-4c98073d93cd/w1_slave'
wire4='/sys/devices/w1_bus_master1/3b-4c98073d951d/w1_slave'
wire5='/sys/devices/w1_bus_master1/3b-4cfc0958f8ce/w1_slave'


# Graphvariablen
fig = plt.Figure(figsize=(8, 4), dpi=80)
fig.patch.set_facecolor('black')
fig.set_tight_layout(True)
ax = fig.add_subplot(111)
fig.suptitle('heatlevel')

#### Klassen und Funktionen ####
# Funktionen zum Wechseln der Seiten:
def switch_page_1_1():
    page_1_1.place(x=0, y=33)
    page_1_2.place_forget()
    page_1_3.place_forget()
    page_1_4.place_forget()
    page_2.place_forget()
    page_3.place_forget()
    page_4.place_forget()
    
def switch_page_1_2():
    page_1_1.place_forget()
    page_1_2.place(x=0, y=33)
    page_1_3.place_forget()
    page_1_4.place_forget()
    page_2.place_forget()
    page_3.place_forget()
    page_4.place_forget()
    
def switch_page_1_3():
    page_1_1.place_forget()
    page_1_2.place_forget()
    page_1_3.place(x=0, y=33)
    page_1_4.place_forget()
    page_2.place_forget()
    page_3.place_forget()
    page_4.place_forget()
    
def switch_page_1_4():
    page_1_1.place_forget()
    page_1_2.place_forget()
    page_1_3.place_forget()
    page_1_4.place(x=0, y=33)
    page_2.place_forget()
    page_3.place_forget()
    page_4.place_forget()
    
def switch_page_2():
    page_1_1.place_forget()
    page_1_2.place_forget()
    page_1_3.place_forget()
    page_1_4.place_forget()
    page_2.place(x=0, y=33)
    page_3.place_forget()
    page_4.place_forget()
    
def switch_page_3():
    page_1_1.place_forget()
    page_1_2.place_forget()
    page_1_3.place_forget()
    page_1_4.place_forget()
    page_2.place_forget()
    page_3.place(x=0, y=33)
    page_4.place_forget()
    
def switch_page_4():
    page_1_1.place_forget()
    page_1_2.place_forget()
    page_1_3.place_forget()
    page_1_4.place_forget()
    page_2.place_forget()
    page_3.place_forget()
    page_4.place(x=0, y=33)

# Funktion zum Berechnen des Füllstands:
def calc_heat ():
    global q, q_rel
    q_max=cp*roh*V_ges*(t_max)/3600
    q_min=cp*roh*V_ges*(t_min)/3600
    q_delta=cp*roh*V_ges*(t_max-t_min)/3600
    q1=cp*roh*(t1.value-t_min)*(V_1/100)*V_ges/3600
    q2=cp*roh*(t2.value-t_min)*(V_1/100)*V_ges/3600
    q3=cp*roh*(t3.value-t_min)*(V_1/100)*V_ges/3600
    q4=cp*roh*(t4.value-t_min)*(V_1/100)*V_ges/3600
    q5=cp*roh*(t5.value-t_min)*(V_1/100)*V_ges/3600
    q=q1+q2+q3+q4+q5
    q_rel=(q/q_delta)*100
    
    ywert=29+390-(q_rel*3.9)
    background_lvl.coords(r_heatlevel,25,ywert,215,419)
    lvl_qrel_h.configure(text=str(int(q_rel)) +' %', fg='white', bg='black', font='Arial')   
    lvl_qrel.configure(text='Gespeicherte Wärmemenge Qrel: '+str(int(q_rel))+' %')
    lvl_qabs.configure(text='Gespeicherte Wärmemenge Qabs: '+str(int(q))+' kWh')
    lvl_qmin.configure(text='Minimale Wärmemenge Qmin: '+str(int(q_min))+' kWh')
    lvl_qmax.configure(text='Maximale Wärmemenge Qmax: '+str(int(q_max))+' kWh')
    lvl_qdelta.configure(text='Maximales Wärmespeichervermögen: '+str(int(q_max-q_min))+' kWh')
    
    main.after(q_time*1000, calc_heat)
    
# lokale Zeit:
def localtime():
    timelbl.configure(text=datetime.today().strftime("%d.%m.%Y %H:%M:%S"))
    main.after(100, localtime)
    
# Auslesend der Temperatur:
def temp_read(pfad, temp):
    with open(pfad) as f:
        f.readline()
        s=f.readline()
    n=s.find('t=')
    if(n>0):
        temp.value=int(s[n+2:])/1000
        
def temp_loop():
    temp_s1=multiprocessing.Process(target=temp_read, args=(wire1, t1))
    temp_s2=multiprocessing.Process(target=temp_read, args=(wire2, t2))
    temp_s3=multiprocessing.Process(target=temp_read, args=(wire3, t3))
    temp_s4=multiprocessing.Process(target=temp_read, args=(wire4, t4))
    temp_s5=multiprocessing.Process(target=temp_read, args=(wire5, t5))
    temp_s1.start()
    temp_s2.start()
    temp_s3.start()
    temp_s4.start()
    temp_s5.start()
    temp_s1.join()
    temp_s2.join()
    temp_s3.join()
    temp_s4.join()
    temp_s5.join()
    temp_t1.configure(text=str(t1.value)+' °C', fg='white', bg='black', font='Arial')
    temp_t2.configure(text=str(t2.value)+' °C', fg='white', bg='black', font='Arial')
    temp_t3.configure(text=str(t3.value)+' °C', fg='white', bg='black', font='Arial')
    temp_t4.configure(text=str(t4.value)+' °C', fg='white', bg='black', font='Arial')
    temp_t5.configure(text=str(t5.value)+' °C', fg='white', bg='black', font='Arial')
    temp_t1_s.configure(text=str(t1.value)+' °C', fg='white', bg='black', font='Arial')
    temp_t2_s.configure(text=str(t2.value)+' °C', fg='white', bg='black', font='Arial')
    temp_t3_s.configure(text=str(t3.value)+' °C', fg='white', bg='black', font='Arial')
    temp_t4_s.configure(text=str(t4.value)+' °C', fg='white', bg='black', font='Arial')
    temp_t5_s.configure(text=str(t5.value)+' °C', fg='white', bg='black', font='Arial')
    temp_sensor_1.itemconfig(temp_sensor_1_c, extent=-(2.7*t1.value))
    temp_sensor_2.itemconfig(temp_sensor_2_c, extent=-(2.7*t2.value))
    temp_sensor_3.itemconfig(temp_sensor_3_c, extent=-(2.7*t3.value))
    temp_sensor_4.itemconfig(temp_sensor_4_c, extent=-(2.7*t4.value))
    temp_sensor_5.itemconfig(temp_sensor_5_c, extent=-(2.7*t5.value))
    main.after(t_time*1000, temp_loop)

# Graph:
def create_graph():    
    ax.set_facecolor('black')            
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='y', colors = 'white')
    ax.set_xlabel('Time', rotation = 0)
    ax.xaxis.label.set_color('white')
    ax.tick_params(axis='x', colors = 'white')        
    ax.set_title('Wärmemenge Q',color='deepskyblue', size=15)
    ax.set_ylabel('Q relativ', rotation = 90, color='deepskyblue',size=15)
    ax.set_xlabel('Zeit T', rotation = 0, color='deepskyblue',size=15)        
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['bottom'].set_color('white')       
    graph_canvas=Canvas(page_4, width= 10, height=10, bd=0, bg='black')
    graph_canvas.place(x=20,y=20)
    canvas = FigureCanvasTkAgg(fig,graph_canvas ) 
    canvas.get_tk_widget().pack() 
    anim = animation.FuncAnimation(fig, animate_graph, frames=1, interval=10000, repeat=True)
    canvas.show()

def animate_graph(i):
    ax.clear()
    ax.set_facecolor('black')           
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='y', colors = 'white')
    ax.set_xlabel('Time', rotation = 0)
    ax.xaxis.label.set_color('white')
    ax.tick_params(axis='x', colors = 'white')    
    ax.set_title('Wärmemenge Q',color='deepskyblue', size=15)
    ax.set_ylabel('Q relativ', rotation = 90, color='deepskyblue',size=15)
    ax.set_xlabel('Zeit T', rotation = 0, color='deepskyblue',size=15)    
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.grid(color ='#a9a9a9', linestyle=':')
    ax.plot(heatlevel)
    ax.set_xticks(range(len(a_time)))
    ax.set_xticklabels(a_time, rotation =45)   
        
    
# Erzeugen der Werte für den Graph:
def create_graph_array():
    global iniv, a_time
    global heatlevel, q_rel, g_time
    timeint=datetime.now()
    zeitplus=timedelta(microseconds=g_time*1000)
    if iniv<10:
        if iniv==0:
            for y in range(0,10,1):
                heatlevel[y]=0
                a_time[y]=timeint.strftime("%H:%M:%S")
                timeint=timeint+zeitplus*1000
        heatlevel[iniv]=int(q_rel)
        iniv=iniv+1
    else:
        for x in range(0,9,1):
            heatlevel[x]=heatlevel[x+1]
            a_time[x]=a_time[x+1]
        heatlevel[9]=q_rel
        a_time[9]=datetime.now().strftime("%H:%M:%S")
    main.after(g_time*1000,create_graph_array)

# Erzeugen einer Datei mit den letzten 24-Stunden:
def create_graph_last_values():
    
    save_intervall=300000 #Wert in Microsekunden 300000=5min
    global heatlevel_l24h, q_rel, a_time_l24h, l24h
    time_l24h=datetime.now()
    zeitplus_l24h=timedelta(microseconds=save_intervall*1000) #speichert den Messwert alle 5 minuten in eine Datei
    print(zeitplus_l24h)
    if l24h<288:
        if l24h==0:
            for y in range(0,288,1):
                heatlevel_l24h[y]=0
                a_time_l24h[y]=time_l24h.strftime("%H:%M:%S")
                time_l24h=time_l24h+zeitplus_l24h
        heatlevel_l24h[l24h]=int(q_rel)
        a_time_l24h[l24h]=datetime.now().strftime("%H:%M:%S")
        l24h=l24h+1
    else:
        for x in range(0,287,1):
            heatlevel_l24h[x]=heatlevel_l24h[x+1]
            a_time_l24h[x]=a_time_l24h[x+1]
        heatlevel_l24h[287]=q_rel
        a_time_l24h[287]=datetime.now().strftime("%H:%M:%S")
    main.after(save_intervall,create_graph_last_values)
    
# Lesefunktionen:
#def read_config():
def read_config():
    config=numpy.load('Config.npy')
    global cp, roh, V_ges,V_1,V_2,V_3,V_4,V_5,t_min,t_max,t_time,q_time,g_time
    cp=float(config[0])
    roh=float(config[1])
    V_ges=950
    V_1=float(config[3])
    V_2=float(config[4])
    V_3=float(config[5])
    V_4=float(config[6])
    V_5=float(config[7])
    t_min=float(config[8])
    t_max=float(config[9])
    t_time=int(config[10])
    q_time=int(config[11])
    g_time=int(config[12])
    #print(t_time)
    #print(type(t_time))

# Speicherfunktionen
def save_graph():
    filename = '/home/pi/Desktop/Füllstandsanzeige/Diagramme/Füllstand_um_'+datetime.now().strftime("%H_%M")+'.pdf'
    fig.savefig(filename, facecolor='black')
    
def save_config():
    config_s=numpy.array([float(opt_cp_e.get()),float(opt_roh_e.get()),950,float(opt_v1_e.get()),float(opt_v2_e.get()),float(opt_v3_e.get()),
                          float(opt_v4_e.get()),float(opt_v5_e.get()),float(opt_tmin_e.get()),float(opt_tmax_e.get()),int(opt_ttime_e.get()),
                          int(opt_qtime_e.get()),int(opt_gtime_e.get())])
    #print(config_s)
    numpy.save('Config',config_s)
    read_config()
    
def save_values():
    l24h_file = open ("/home/pi/Desktop/Füllstandsanzeige/Messwerte/messwerte_"+datetime.now().strftime("%H_%M")+'.txt', 'a')
    l24h_file.write('Nr.')
    l24h_file.write("\t")
    l24h_file.write('Qrel')
    l24h_file.write("\t")
    l24h_file.write('t')
    l24h_file.write("\n")
    for line in range (0, 288, 1):
        l24h_file.write(str(line))
        l24h_file.write("\t")
        l24h_file.write(str(heatlevel_l24h[line]))
        l24h_file.write("\t")
        l24h_file.write(str(a_time_l24h[line]))
        l24h_file.write("\n")
    print(heatlevel_l24h)
    l24h_file.close()
    


#### Tkinter Hauptprogramm ####
if __name__ == '__main__':
    main = Tk()
    main.title("Temperaturverlauf")
    main.geometry('800x480')
    main.attributes('-fullscreen',True)
    main.configure(bg='black')
    main.config(cursor='none')
    read_config()
        
    # Bilder erzeugen
    pic_option=PhotoImage(file='/home/pi/Desktop/Füllstandsanzeige/graphische Elemente/pic_option.png')
    pic_next=PhotoImage(file='/home/pi/Desktop/Füllstandsanzeige/graphische Elemente/pic_next.png')
    pic_last=PhotoImage(file='/home/pi/Desktop/Füllstandsanzeige/graphische Elemente/pic_last.png')
    pic_progressbar=PhotoImage(file='/home/pi/Desktop/Füllstandsanzeige/graphische Elemente/pic_progressbar.png')
    pic_sensortemp=PhotoImage(file='/home/pi/Desktop/Füllstandsanzeige/graphische Elemente/pic_sensortemp.png')
    pic_graph=PhotoImage(file='/home/pi/Desktop/Füllstandsanzeige/graphische Elemente/pic_graph.png')
    pic_download=PhotoImage(file='/home/pi/Desktop/Füllstandsanzeige/graphische Elemente/pic_download.png')
    pic_save=PhotoImage(file='/home/pi/Desktop/Füllstandsanzeige/graphische Elemente/pic_save.png')
    pic_exit=PhotoImage(file='/home/pi/Desktop/Füllstandsanzeige/graphische Elemente/pic_exit.png')
    pic_wifi=PhotoImage(file='/home/pi/Desktop/Füllstandsanzeige/graphische Elemente/pic_wifi.png')
    pic_dim=PhotoImage(file='/home/pi/Desktop/Füllstandsanzeige/graphische Elemente/pic_dim.png')
    pic_sensorpos=PhotoImage(file='/home/pi/Desktop/Füllstandsanzeige/graphische Elemente/pic_sensorpos.png')
    pic_sensor_ol=PhotoImage(file='/home/pi/Desktop/Füllstandsanzeige/graphische Elemente/pic_sensor_ol.png')
    pic_progressbar_ol=PhotoImage(file='/home/pi/Desktop/Füllstandsanzeige/graphische Elemente/pic_progressbar_ol.png')
    pic_hska=PhotoImage(file='/home/pi/Desktop/Füllstandsanzeige/graphische Elemente/pic_hska.png')
    pic_ikku=PhotoImage(file='/home/pi/Desktop/Füllstandsanzeige/graphische Elemente/pic_ikku.png')
    
    
    # Erzeugen der Buttons
    button_option=Button(main, image=pic_option, bg='black', bd=0, highlightcolor='black', highlightbackground='black',activebackground='black', command=switch_page_1_1)
    button_progressbar=Button(main, image=pic_progressbar, bg='black', bd=0, highlightcolor='black', highlightbackground='black',activebackground='black', command=switch_page_2)
    button_sensortemp=Button(main, image=pic_sensortemp, bg='black', bd=0, highlightcolor='black', highlightbackground='black',activebackground='black', command=switch_page_3)
    button_graph=Button(main, image=pic_graph, bg='black', bd=0, highlightcolor='black', highlightbackground='black',activebackground='black', command=switch_page_4)

    button_option.place(x=710,y=56)
    button_progressbar.place(x=710,y=162)
    button_sensortemp.place(x=710,y=268)
    button_graph.place(x=710,y=374)
    
    # Taskleiste:
    background_tsk=Canvas(main, width='810', height='40', bd=0, bg='black', highlightthickness=0)
    background_tsk.create_line(0,36, 810, 36, fill='#00B0F0', width='2')
    background_tsk.place(x=-5, y=-5)
    timelbl=Label(main, fg='#00B0F0', bg='black', font='Arial')
    timelbl.place(x=10,y=6)
    localtime()
    
    # Erzeugen der Frames
    page_1_1=Frame(main, width=710, height=448, bg='black')
    page_1_2=Frame(main, width=710, height=448, bg='black')
    page_1_3=Frame(main, width=710, height=448, bg='black')
    page_1_4=Frame(main, width=710, height=448, bg='black')
    page_2=Frame(main, width=710, height=448, bg='black')
    page_3=Frame(main, width=710, height=448, bg='red')
    page_4=Frame(main, width=710, height=448, bg='black')
    page_1_1.place(x=0, y=33)
    
    # Seite 1.1: Einstellungen - Prozessparameter
    background_opt=Canvas(page_1_1, width='720', height='455', bd=0, bg='black', highlightthickness=0)
    background_opt.place(x=0,y=0)
    background_opt.create_line(25,45, 500, 45, fill='#00B0F0', width='2')
    background_opt.create_line(25,167, 500, 167, fill='#00B0F0', width='2')
    background_opt.create_line(25,289, 500, 289, fill='#00B0F0', width='2')
    # Seite 1.1: Einstellungen - Buttons
    button_next=Button(page_1_1, image=pic_next, bg='black', bd=0, highlightcolor='black', highlightbackground='black',activebackground='black', command=switch_page_1_2)
    button_last=Button(page_1_1, image=pic_last, bg='black', bd=0, highlightcolor='black', highlightbackground='black',activebackground='black', command=switch_page_1_4)
    button_save=Button(page_1_1, image=pic_save, bg='black', bd=0, highlightcolor='black', highlightbackground='black',activebackground='black', command=save_config)
    button_next.place(x=648,y=381)
    button_last.place(x=604,y=381)
    button_save.place(x=532,y=386)
    # Seite 1.1: Stoffdaten
    opt_title_1=Label(page_1_1, text='Stoffdaten: ', fg='#00B0F0', bg='black', font='Arial')
    opt_title_1.place(x=25, y=22)
    opt_cp_l=Label(page_1_1, text='Spezifische Wärmekapazität: ', fg='white', bg='black', font='Arial')
    opt_cp_l.place(x=25, y=58)
    opt_cp_d=Label(page_1_1, text='kJ/(kg*K)', fg='white', bg='black', font='Arial')
    opt_cp_d.place(x=360, y=58)
    opt_cp_e=Entry(page_1_1, bd=1, fg='white', bg='black', font='Arial', width='10')
    opt_cp_e.place(x=250, y=58)
    opt_cp_e.insert(0, cp)
    opt_roh_l=Label(page_1_1, text='Dichte : ', fg='white', bg='black', font='Arial')
    opt_roh_l.place(x=25, y=92)
    opt_roh_d=Label(page_1_1, text='kg/dm³', fg='white', bg='black', font='Arial')
    opt_roh_d.place(x=360, y=92)
    opt_roh_e=Entry(page_1_1, bd=1, fg='white', bg='black', font='Arial', width='10')
    opt_roh_e.place(x=250, y=92)
    opt_roh_e.insert(0, roh)
    # Seite 1.1: Randbedingungen
    opt_title_2=Label(page_1_1, text='Randbedingungen: ', fg='#00B0F0', bg='black', font='Arial')
    opt_title_2.place(x=25, y=144)
    opt_tmin_l=Label(page_1_1, text='minimale Temperatur: ', fg='white', bg='black', font='Arial')
    opt_tmin_l.place(x=25, y=180)
    opt_tmin_d=Label(page_1_1, text='°C', fg='white', bg='black', font='Arial')
    opt_tmin_d.place(x=360, y=180)
    opt_tmin_e=Entry(page_1_1, bd=1, fg='white', bg='black', font='Arial', width='10')
    opt_tmin_e.place(x=250, y=180)
    opt_tmin_e.insert(0, t_min)
    opt_tmax_l=Label(page_1_1, text='maximale Temperatur: ', fg='white', bg='black', font='Arial')
    opt_tmax_l.place(x=25, y=214)
    opt_tmax_d=Label(page_1_1, text='°C', fg='white', bg='black', font='Arial')
    opt_tmax_d.place(x=360, y=214)
    opt_tmax_e=Entry(page_1_1, bd=1, fg='white', bg='black', font='Arial', width='10')
    opt_tmax_e.place(x=250, y=214)
    opt_tmax_e.insert(0, t_max)
    # Seite 1.1: Ausleseintervall
    opt_title_1=Label(page_1_1, text='Abtastintervalle: ', fg='#00B0F0', bg='black', font='Arial')
    opt_title_1.place(x=25, y=266)
    opt_ttime_l=Label(page_1_1, text='Abtastintervall Temperatur: ', fg='white', bg='black', font='Arial')
    opt_ttime_l.place(x=25, y=302)
    opt_ttime_d=Label(page_1_1, text='s', fg='white', bg='black', font='Arial')
    opt_ttime_d.place(x=360, y=302)
    opt_ttime_e=Entry(page_1_1,text=t_min, bd=1, fg='white', bg='black', font='Arial', width='10')
    opt_ttime_e.place(x=250, y=302)
    opt_ttime_e.insert(0, t_time)
    opt_qtime_l=Label(page_1_1, text='Abtastintervall Wärmemenge: ', fg='white', bg='black', font='Arial')
    opt_qtime_l.place(x=25, y=336)
    opt_qtime_d=Label(page_1_1, text='s', fg='white', bg='black', font='Arial')
    opt_qtime_d.place(x=360, y=336)
    opt_qtime_e=Entry(page_1_1, bd=1, fg='white', bg='black', font='Arial', width='10')
    opt_qtime_e.place(x=250, y=336)
    opt_qtime_e.insert(0, q_time)
    opt_gtime_l=Label(page_1_1, text='Aktualisierungsintervall Graph: ', fg='white', bg='black', font='Arial')
    opt_gtime_l.place(x=25, y=370)
    opt_gtime_d=Label(page_1_1, text='s', fg='white', bg='black', font='Arial')
    opt_gtime_d.place(x=360, y=370)
    opt_gtime_e=Entry(page_1_1, bd=1, fg='white', bg='black', font='Arial', width='10')
    opt_gtime_e.place(x=250, y=370)
    opt_gtime_e.insert(0, g_time)  
    ### Seite 1.2: Einstellungen - Geometrie
    background_opt2=Canvas(page_1_2, width='720', height='455', bd=0, bg='black', highlightthickness=0)
    background_opt2.place(x=0,y=0)
    background_opt2.create_line(440,45, 680, 45, fill='#00B0F0', width='2')
    background_opt2.create_image(25,29, image=pic_dim, anchor='nw')
    button_next=Button(page_1_2, image=pic_next, bg='black', bd=0, highlightcolor='black', highlightbackground='black',activebackground='black', command=switch_page_1_3)
    button_last=Button(page_1_2, image=pic_last, bg='black', bd=0, highlightcolor='black', highlightbackground='black',activebackground='black', command=switch_page_1_1)
    button_save=Button(page_1_2, image=pic_save, bg='black', bd=0, highlightcolor='black', highlightbackground='black',activebackground='black', command=save_config)
    button_next.place(x=648,y=381)
    button_last.place(x=604,y=381)
    button_save.place(x=532,y=386)
    # Seite 1.2: Volumeneinstellungen
    opt_title_1=Label(page_1_2, text='Volumeneinstellungen: ', fg='#00B0F0', bg='black', font='Arial')
    opt_title_1.place(x=440, y=22)
    opt_v1_l=Label(page_1_2, text='Relatives Volumen V5: ', fg='white', bg='black', font='Arial')
    opt_v1_l.place(x=440, y=58)
    opt_v1_d=Label(page_1_2, text='%', fg='white', bg='black', font='Arial')
    opt_v1_d.place(x=655, y=58)
    opt_v1_e=Entry(page_1_2, bd=1, fg='white', bg='black', font='Arial', width='4')
    opt_v1_e.place(x=610, y=58)
    opt_v1_e.insert(0, V_5)
    opt_v2_l=Label(page_1_2, text='Relatives Volumen V4: ', fg='white', bg='black', font='Arial')
    opt_v2_l.place(x=440, y=92)
    opt_v2_d=Label(page_1_2, text='%', fg='white', bg='black', font='Arial')
    opt_v2_d.place(x=655, y=92)
    opt_v2_e=Entry(page_1_2, bd=1, fg='white', bg='black', font='Arial', width='4')
    opt_v2_e.place(x=610, y=92)
    opt_v2_e.insert(0, V_2)
    opt_v3_l=Label(page_1_2, text='Relatives Volumen V3: ', fg='white', bg='black', font='Arial')
    opt_v3_l.place(x=440, y=126)
    opt_v3_d=Label(page_1_2, text='%', fg='white', bg='black', font='Arial')
    opt_v3_d.place(x=655, y=126)
    opt_v3_e=Entry(page_1_2, bd=1, fg='white', bg='black', font='Arial', width='4')
    opt_v3_e.place(x=610, y=126)
    opt_v3_e.insert(0, V_3)
    opt_v4_l=Label(page_1_2, text='Relatives Volumen V2: ', fg='white', bg='black', font='Arial')
    opt_v4_l.place(x=440, y=160)
    opt_v4_d=Label(page_1_2, text='%', fg='white', bg='black', font='Arial')
    opt_v4_d.place(x=655, y=160)
    opt_v4_e=Entry(page_1_2, bd=1, fg='white', bg='black', font='Arial', width='4')
    opt_v4_e.place(x=610, y=160)
    opt_v4_e.insert(0, V_4)
    opt_v5_l=Label(page_1_2, text='Relatives Volumen V1: ', fg='white', bg='black', font='Arial')
    opt_v5_l.place(x=440, y=194)
    opt_v5_d=Label(page_1_2, text='%', fg='white', bg='black', font='Arial')
    opt_v5_d.place(x=655, y=194)
    opt_v5_e=Entry(page_1_2, bd=1, fg='white', bg='black', font='Arial', width='4')
    opt_v5_e.place(x=610, y=194)
    opt_v5_e.insert(0, V_5)
    opt_vges_l=Label(page_1_2, text='Gesamtvolumen : '+str(V_ges)+' liter', fg='white', bg='black', font='Arial')
    opt_vges_l.place(x=440, y=228)
    ### Seite 1.3: Einstellungen - Sensorpositionen
    background_opt3=Canvas(page_1_3, width='720', height='455', bd=0, bg='black', highlightthickness=0)
    background_opt3.place(x=0,y=0)
    background_opt3.create_line(440,45, 680, 45, fill='#00B0F0', width='2')
    background_opt3.create_image(25,29, image=pic_dim, anchor='nw')
    button_next=Button(page_1_3, image=pic_next, bg='black', bd=0, highlightcolor='black', highlightbackground='black',activebackground='black', command=switch_page_1_4)
    button_last=Button(page_1_3, image=pic_last, bg='black', bd=0, highlightcolor='black', highlightbackground='black',activebackground='black', command=switch_page_1_2)
    button_next.place(x=648,y=381)
    button_last.place(x=604,y=381)
    # Seite 1.3: Höheneinstellungen
    opt_title_1=Label(page_1_3, text='Positionen der Sensoren: ', fg='#00B0F0', bg='black', font='Arial')
    opt_title_1.place(x=440, y=22)
    opt_v1_l=Label(page_1_3, text='Höhenmaß h5: 1600 mm', fg='white', bg='black', font='Arial')
    opt_v1_l.place(x=440, y=58)
    opt_v2_l=Label(page_1_3, text='Höhenmaß h4: 1200 mm', fg='white', bg='black', font='Arial')
    opt_v2_l.place(x=440, y=92)
    opt_v3_l=Label(page_1_3, text='Höhenmaß h3:   820 mm', fg='white', bg='black', font='Arial')
    opt_v3_l.place(x=440, y=126)
    opt_v4_l=Label(page_1_3, text='Höhenmaß h2:   680 mm', fg='white', bg='black', font='Arial')
    opt_v4_l.place(x=440, y=160)
    opt_v5_l=Label(page_1_3, text='Höhenmaß h1:   480 mm', fg='white', bg='black', font='Arial')
    opt_v5_l.place(x=440, y=194)
    ### Seite 1.4: Beenden
    background_opt4=Canvas(page_1_4, width='720', height='455', bd=0, bg='black', highlightthickness=0)
    background_opt4.place(x=0,y=0)
    background_opt4.create_image(25,29, image=pic_hska, anchor='nw')
    background_opt4.create_image(25,270, image=pic_ikku, anchor='nw')
    
    button_next=Button(page_1_4, image=pic_next, bg='black', bd=0, highlightcolor='black', highlightbackground='black',activebackground='black', command=switch_page_1_1)
    button_last=Button(page_1_4, image=pic_last, bg='black', bd=0, highlightcolor='black', highlightbackground='black',activebackground='black', command=switch_page_1_3)
    button_exit=Button(page_1_4, image=pic_exit, bg='black', bd=0, highlightcolor='black', highlightbackground='black',activebackground='black', command=lambda:main.destroy())
    button_next.place(x=648,y=381)
    button_last.place(x=604,y=381)
    button_exit.place(x=604,y=24)
    
    #### Seite 2: Füllstand
    background_lvl=Canvas(page_2, width='720', height='455', bd=0, bg='black', highlightthickness=0)
    background_lvl.place(x=0,y=0)
    background_lvl.create_line(240,45, 680, 45, fill='#00B0F0', width='2')
    r_heatlevel=background_lvl.create_rectangle(25,29,419,215,fill='#00B0F0')
    background_lvl.create_image(25,29, image=pic_progressbar_ol, anchor='nw')
    lvl_title_1=Label(page_2, text='Angaben zur Wärmemenge: ', fg='#00B0F0', bg='black', font='Arial')
    lvl_title_1.place(x=240, y=22)
    
    lvl_qrel=Label(page_2, text='Gespeicherte Wärmemenge Qrel: ', fg='white', bg='black', font='Arial')
    lvl_qrel.place(x=240, y=58)
    lvl_qabs=Label(page_2, text='Gespeicherte Wärmemenge Qabs:', fg='white', bg='black', font='Arial')
    lvl_qabs.place(x=240, y=92)
    lvl_qmin=Label(page_2, text='Minimale Wärmemenge Qmin: ', fg='white', bg='black', font='Arial')
    lvl_qmin.place(x=240, y=126)
    lvl_qmax=Label(page_2, text='Maximale Wärmemenge Qmax: ', fg='white', bg='black', font='Arial')
    lvl_qmax.place(x=240, y=160)
    lvl_qdelta=Label(page_2, text='Maximales Wärmespeichervermögen: ', fg='white', bg='black', font='Arial')
    lvl_qdelta.place(x=240, y=194)
    
    lvl_qrel_h=Label(page_2,)
    lvl_qrel_h.place(x=90,y=210)
    
    #### Seite 3: Temperaturen
    background_temp=Canvas(page_3, width='720', height='455', bd=0, bg='black', highlightthickness=0)
    background_temp.place(x=0,y=0)
    background_temp.create_line(240,45, 680, 45, fill='#00B0F0', width='2')
    background_temp.create_image(25,29, image=pic_sensorpos, anchor='nw')
    
    temp_title_1=Label(page_3, text='Sensortemperaturen: ', fg='#00B0F0', bg='black', font='Arial')
    temp_title_1.place(x=240, y=22)
    
    temp_sensor_1=Canvas(page_3, width='128', height='96', bd=0, bg='grey', highlightthickness=0)
    temp_sensor_1.place(x=250,y=92)
    temp_sensor_1_c=temp_sensor_1.create_arc(0,0,128,115, fill='#00B0F0', start=225, extent=-180)
    temp_sensor_1.create_image(0,0, image=pic_sensor_ol, anchor='nw')
    temp_sensor_1_l=Label(page_3, text='Sensor T1: ', fg='white', bg='black', font='Arial')
    temp_sensor_1_l.place(x=270, y=58)
    
    temp_sensor_2=Canvas(page_3, width='128', height='96', bd=0, bg='grey', highlightthickness=0)
    temp_sensor_2.place(x=398,y=92)
    temp_sensor_2_c=temp_sensor_2.create_arc(0,0,128,115, fill='#00B0F0', start=225, extent=-50)
    temp_sensor_2.create_image(0,0, image=pic_sensor_ol, anchor='nw')
    temp_sensor_2_l=Label(page_3, text='Sensor T2: ', fg='white', bg='black', font='Arial')
    temp_sensor_2_l.place(x=418, y=58)
    
    temp_sensor_3=Canvas(page_3, width='128', height='96', bd=0, bg='grey', highlightthickness=0)
    temp_sensor_3.place(x=546,y=92)
    temp_sensor_3_c=temp_sensor_3.create_arc(0,0,128,115, fill='#00B0F0', start=225, extent=-180)
    temp_sensor_3.create_image(0,0, image=pic_sensor_ol, anchor='nw')
    temp_sensor_3_l=Label(page_3, text='Sensor T3: ', fg='white', bg='black', font='Arial')
    temp_sensor_3_l.place(x=566, y=58)
    
    temp_sensor_4=Canvas(page_3, width='128', height='96', bd=0, bg='grey', highlightthickness=0)
    temp_sensor_4.place(x=250,y=256)
    temp_sensor_4_c=temp_sensor_4.create_arc(0,0,128,115, fill='#00B0F0', start=225, extent=-180)
    temp_sensor_4.create_image(0,0, image=pic_sensor_ol, anchor='nw')
    temp_sensor_4_l=Label(page_3, text='Sensor T4: ', fg='white', bg='black', font='Arial')
    temp_sensor_4_l.place(x=270, y=222)

    temp_sensor_5=Canvas(page_3, width='128', height='96', bd=0, bg='grey', highlightthickness=0)
    temp_sensor_5.place(x=398,y=256)
    temp_sensor_5_c=temp_sensor_5.create_arc(0,0,128,115, fill='#00B0F0', start=225, extent=-180)
    temp_sensor_5.create_image(0,0, image=pic_sensor_ol, anchor='nw')
    temp_sensor_5_l=Label(page_3, text='Sensor T5: ', fg='white', bg='black', font='Arial')
    temp_sensor_5_l.place(x=418, y=222)

    temp_t1=Label(page_3 )
    temp_t1.place(x=282, y=135)
    temp_t2=Label(page_3)
    temp_t2.place(x=430, y=135)
    temp_t3=Label(page_3)
    temp_t3.place(x=578, y=135)
    temp_t4=Label(page_3)
    temp_t4.place(x=282, y=300)
    temp_t5=Label(page_3)
    temp_t5.place(x=430, y=300)
    
    temp_t1_s=Label(page_3 )
    temp_t1_s.place(x=90, y=365)
    temp_t2_s=Label(page_3)
    temp_t2_s.place(x=90, y=290)
    temp_t3_s=Label(page_3)
    temp_t3_s.place(x=90, y=215)
    temp_t4_s=Label(page_3)
    temp_t4_s.place(x=90, y=135)
    temp_t5_s=Label(page_3)
    temp_t5_s.place(x=90, y=70)
    
    #### Seite 4: Graphen
    button_save_graph=Button(page_4, image=pic_download, bg='black', bd=0, highlightcolor='black', highlightbackground='black',activebackground='black', command=save_graph)
    button_save_values=Button(page_4, image=pic_save, bg='black', bd=0, highlightcolor='black', highlightbackground='black',activebackground='black', command=save_values)
    lbl_save_graph=Label(page_4, text='Graph Speichern: ', fg='white', bg='black', font='Arial')
    lbl_save_value=Label(page_4, text='Messwerte Speichern: ', fg='white', bg='black', font='Arial')  
    lbl_save_graph.place(x=300,y=390)
    lbl_save_value.place(x=30,y=390)
    button_save_graph.place(x=440,y=381)
    button_save_values.place(x=200,y=381)
    
    temp_loop()
    calc_heat()
    create_graph_array()
    create_graph_last_values()
    create_graph()

    
    main.mainloop()
    
    
    
    
    
