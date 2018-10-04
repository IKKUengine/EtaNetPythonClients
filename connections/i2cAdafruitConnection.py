import threading
#import Adafruit_ADS1x15

class I2cAdafruitConnection(threading.Thread):

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


    def __init__(self):

        threading.Thread.__init__(self)

        # Create an ADS1115 ADC (16-bit) instance.
        self.adc = 1
            #= Adafruit_ADS1x15.ADS1115()

        # Note you can change the I2C address from its default (0x48), and/or the I2C
        # bus by passing in these optional parameters:
        # adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

    def run(self):
        #self.lock.acquire()
        self.request()
        #self.lock.release()

    def request(self):
        pass




