import parameter
import meterbus
from connections import networkConnection
from observer import observe
import datetime
import re

class HeatMeter(networkConnection.MBusConnection, observe.Observer):

    dataStr = "(TimeStamp; Heat Meter; Value1; Unit1; Value2; Unit2)"

    def __init__(self, observable, primeAdress):
        networkConnection.MBusConnection.__init__(self, '192.168.178.66', 10001, primeAdress)
        observe.Observer.__init__(self, observable)
        #Regular expression operations to find all scientific numbers
        self.match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
        self.addr = primeAdress

    def notify(self):
        return self.dataStr

    def request(self):
        data = self.getAllData(self.addr)
        powerTs = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
#        testData = "\x68\x71\x71\x68\x08\x02\x72\x49\x01\x19\x10\x49\x6A\x88\x04\xBE" \
#                "\x00\x00\x00\x0C\x78\x49\x01\x19\x10\x04\x06\x01\x00\x00" \
#                "\x00\x82\x04\x6C\x41\x21\xC2\x84\x00\x6C\xFF\xFF\x84\x04\x06\x00" \
#                "\x00\x00\x00\xC4\x84\x00\x06\x00\x00\x00\x80\x82\x0A\x6C\x41\x29\x84\x0A" \
#                "\x06\x00\x00\x00\x00\x04\x13\x18\x02\x00\x00\x02\x59\xA4\x08\x02\x5D\x16\x09" \
#                "\x02\x61\x00\x00\x04\x2D\x00\x00\x00\x00\x04\x3B\x00\x00\x00\x00\x04\x6D\x1A" \
#                "\x0A\x59\x29\x04\x26\x44\x18\x00\x00\x02\xFD\x17\x00\x00\x1F\x9F\x16"

        telegram = meterbus.load(data)
        #Instabilities/bugs of meterbus lib/package
        find3 = [float(x) for x in re.findall(self.match_number, str(telegram.records[13].interpreted) + str(telegram.records[13].interpreted))]
        if find3[0] == 3:
            replace = find3[1]
        else:
            replace = find3[0]

        powList = [float(x) for x in re.findall(self.match_number, str(telegram.records[12].interpreted) \
                  + str(telegram.records[13].interpreted) + str(telegram.records[9].interpreted) \
                  + str(telegram.records[10].interpreted))]
        
        if parameter.printMessages:
            print("Adresse: " + str(self.addr))
            print (str(telegram.records[0].interpreted) + "\n" \
                                    + str(telegram.records[1].interpreted) + "\n" \
                                    + str(telegram.records[2].interpreted) + "\n" \
                                    + str(telegram.records[3].interpreted) + "\n" \
                                    + str(telegram.records[4].interpreted) + "\n" \
                                    + str(telegram.records[5].interpreted) + "\n" \
                                    + str(telegram.records[6].interpreted) + "\n" \
                                    + str(telegram.records[7].interpreted) + "\n" \
                                    + str(telegram.records[8].interpreted) + "\n" \
                                    + str(telegram.records[9].interpreted) + "\n" \
                                    + str(telegram.records[10].interpreted) + "\n" \
                                    + str(telegram.records[11].interpreted) + "\n" \
                                    + str(telegram.records[12].interpreted) + "\n" \
                                    + replace + "\n" \
                                    + str(telegram.records[14].interpreted) + "\n" \
                                    + str(telegram.records[15].interpreted) + "\n" \
                                    + str(telegram.records[16].interpreted))
        try:
            self.dataStr = "({}; Heat Meter {}; {:8.6f}; {}; {:8.6f}; {}; {:8.6f}; {}; {:8.6f}; {})".format(powerTs, \
                           self.addr, powList[0], "[W]", replace, "[m³/h]", powList[3], "[T_Flow]", powList[4], \
                           "[T_Return]")
        except:
            print ("Heat Meter {} is switched off!".format(self.addr))

    def getData(self):
        return self.dataStr