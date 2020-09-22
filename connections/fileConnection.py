import time
import threading
import parameter
import glob
import RPi.GPIO as GPIO #added

class FileConnection(threading.Thread):
    
    exit = True
    stop = True


    def __init__(self):
        threading.Thread.__init__(self)
        
        # the one-wire input pin will be declared and the integrated pullup-resistor will be enabled
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        base_dir = '/sys/bus/w1/devices/'
        while True:
            try:
                device_folder = glob.glob(base_dir + '28*')[0]
                break
            except IndexError:
                sleep(0.5)
                continue
        self.device_file = device_folder + '/w1_slave'

        
        if parameter.printMessages:
            print("init file connection")
        threading.Thread.start(self)

    def run(self):
        #self.lock.acquire()
        while self.exit:#threat wird erst beendet wenn aus while schleife herausgeganen wird
            if self.stop:
                self.request()
            time.sleep(parameter.timeTriggerPowerAnalayser)
            #self.lock.release()

    def request(self):
        pass
    
    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self,lines):
        #lines = read_temp_raw(self,device_file)
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            TempIn = float(temp_string) / 1000.0
            #temp_f = temp_c * 9.0 / 5.0 + 32.0     if you want use Fahrenheit, modify these lines  
            return TempIn
    
    def getSerialPort(self):
        return self.__ser

    def setStop(self):
        self.stop = False

    def setStart(self):
        self.stop = True

    def setExit(self):
        self.exit = False
        
    def __exit__(self):
        pass