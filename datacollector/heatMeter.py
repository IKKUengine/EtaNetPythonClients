import error
import meterbus
from connections import networkConnection
from observer import observe

class HeatMeter(networkConnection.MBusConnection, observe.Observer):

    dataStr = "(TimeStamp; Heat Meter; Value1; Unit1; Value2; Unit2)"

    def __init__(self, observable, primeAdress):
       # rs232Connection.Rs232Connection.__init__()
        #observe.Observer.__init__(observable)
        networkConnection.MBusConnection.__init__(self, '192.168.178.66', 10001, primeAdress)
        observe.Observer.__init__(self, observable)
        self.addr = primeAdress

    def notify(self):
        return self.dataStr

    def request(self):
        #self.infoText['text'] = 'Heat Meter 2 (Warmwasser) muss noch implementiert werden...'
        
        
        data4 = self.getAllData(self.addr)
        if error.printMessages:
            print (data4)
        
        data = "\x68\x6A\x6A\x68\x08\x01\x72\x43\x53\x93\x07\x65" \
               "\x32\x10\x04\xCA\x00\x00\x00\x0C\x05\x14\x00\x00" \
               "\x00\x0C\x13\x13\x20\x00\x00\x0B\x22\x01\x24\x03" \
               "\x04\x6D\x12\x0B\xD3\x12\x32\x6C\x00\x00\x0C\x78" \
               "\x43\x53\x93\x07\x06\xFD\x0C\xF2\x03\x01\x00\xF6" \
               "\x01\x0D\xFD\x0B\x05\x31\x32\x4D\x46\x57\x01\xFD" \
               "\x0E\x00\x4C\x05\x14\x00\x00\x00\x4C\x13\x13\x20" \
               "\x00\x00\x42\x6C\xBF\x1C\x0F\x37\xFD\x17\x00\x00" \
               "\x00\x00\x00\x00\x00\x00\x02\x7A\x25\x00\x02\x78" \
               "\x25\x00\x3A\x16"

        data2 = "\x68\x71\x71\x68\x08\x02\x72\x49\x01\x19" \
                "\x10\x49\x6A\x88\x04\x8B" \
                "\x00\x00\x00\x0C\x78\x49\x01\x19\x10\x04" \
                "\x06\x01\x00\x00\x00\x82" \
                "\x04\x6C\x41\x21\xC2\x84\x00\x6C\xFF\xFF" \
                "\x84\x04\x06\x00\x00\x00" \
                "\x00\xC4\x84\x00\x06\x00\x00\x00\x80\x82" \
                "\x0A\x6C\x41\x29x84\x0A" \
                "\x06\x00\x00\x00\x00\x04" \
                "\x13\x18\x02\x00\x00\x02\x59\xDB\x07\x02" \
                "\x5D\xB2\x07\x02\x61\x29\x00\x04" \
                "\x2D\x00\x00\x00\x00\x04\x3B\x00" \
                "\x00\x00\x00\x04\x6D\x11\x0D\x58\x29\x04" \
                "\x26\x2F\x18\x00\x00\x02" \
                "\xFD\x17\x00\x00\x1F\x49\x16"

        data3 = "\x68\x71\x71\x68\x08\x02\x72\x49\x01\x19\x10\x49\x6A\x88\x04\xBE" \
                "\x00\x00\x00\x0C\x78\x49\x01\x19\x10\x04\x06\x01\x00\x00" \
                "\x00\x82\x04\x6C\x41\x21\xC2\x84\x00\x6C\xFF\xFF\x84\x04\x06\x00" \
                "\x00\x00\x00\xC4\x84\x00\x06\x00\x00\x00\x80\x82\x0A\x6C\x41\x29\x84\x0A" \
                "\x06\x00\x00\x00\x00\x04\x13\x18\x02\x00\x00\x02\x59\xA4\x08\x02\x5D\x16\x09" \
                "\x02\x61\x00\x00\x04\x2D\x00\x00\x00\x00\x04\x3B\x00\x00\x00\x00\x04\x6D\x1A" \
                "\x0A\x59\x29\x04\x26\x44\x18\x00\x00\x02\xFD\x17\x00\x00\x1F\x9F\x16"
        
        #data4 = self.getData("")
        #pirnt ("Data4: "+ data4)

        telegram = meterbus.load(data4)
        if error.printMessages:
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
                                    + str(telegram.records[13].interpreted) + "\n" \
                                    + str(telegram.records[14].interpreted) + "\n" \
                                    + str(telegram.records[15].interpreted) + "\n" \
                                    + str(telegram.records[16].interpreted))

        #getData() 