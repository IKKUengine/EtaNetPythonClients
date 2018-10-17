
from connections import i2cAdafruitConnection
from observer import observe
import parameter
import datetime

class MassFlow(i2cAdafruitConnection.I2cAdafruitConnection, observe.Observer):

    dataStr = "(TimeStamp; Gas Mass Flow; Value1; Unit1; Value2; Unit2)"

    def __init__(self, observable):
       # rs232Connection.Rs232Connection.__init__()
        #observe.Observer.__init__(observable)
        i2cAdafruitConnection.I2cAdafruitConnection.__init__(self)
        observe.Observer.__init__(self, observable)

    def notify(self):
      return self.dataStr

    def request(self):
        # Read all the ADC channel values in a list.
        values = [0] * 4
        # for i in range(4):
        # Read the specified ADC channel using the previously set gain value.
        values[0] = self.adc.read_adc(0, gain=self.GAIN)
        powerTs = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # values[1] = adc.read_adc(1, gain=GAIN)
        # values[2] = adc.read_adc(2, gain=GAIN)
        # values[3] = adc.read_adc(3, gain=GAIN)
        # Note you can also pass in an optional data_rate parameter that controls
        # the ADC conversion time (in samples/second). Each chip has a different
        # set of allowed data rate values, see datasheet Table 9 config register
        # DR bit values.
        # values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
        # Each value will be a 16 bit signed integer value depending on the
        # ADC (ADS1115 = 16-bit).

        # Calculation and calibration of the gas fuel flow
        fuelflow = (values[0]) / (2 * 3276.8) * 4.2 * 0.046166667
        if parameter.printMessages:
            print ("Fuel flow [kg/h]: " + str(fuelflow))
        try:
            self.dataStr = "({}; Gas Mass Flow; {:8.6f}; {})".format(powerTs, fuelflow, "[kg/h]")       
        except:
            print ("Gas Mass Flow Sensor is switched off!")
        
    def getData(self):
        return self.dataStr
                   