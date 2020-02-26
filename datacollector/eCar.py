from observer import observe
from connections import canConnection
import parameter
import datetime
import re
import numpy as np

class ECar(canConnection.CANConnection, observe.Observer):

    dataStr = "'NaN', 'NaN'"
    headerStr = "'SoC [%]', 'SoH [%]'"
 

    def __init__(self, observable):
       # rs232Connection.Rs232Connection.__init__()
        #observe.Observer.__init__(observable)
        canConnection.CANConnection.__init__(self)
        observe.Observer.__init__(self, observable)

    def notifyData(self):
      return self.dataStr
    
    def notifyHeader(self):
      return self.headerStr

    def request(self):
        
        #try:
            
        #___________________________SoC__________________________________
        
        self.getCanPort().send(self.getMessageSoC())
        # response should be can_id=0x607, data=[0xF1, 0x06, 0x62, 0xDD, 0xC4, 0xdata1, 0xdata2, 0x01]
        #print("SoC Message sent")
        
        # filter unnecessary codes from other buses, but can't fully filter because the can-library can't fully do it
        self.getCanPort().set_filters([{"can_id":0x607, "can_mask":0xF1, "extended":False}]) 
        SoC_all_data = self.getCanPort().recv()
#             print(SoC_all_data)

        #______prepare for manual filtering______
        #create an array, then string for filtering
        SoC_data_array=np.array([SoC_all_data])
        SoC_data_string= str(SoC_data_array)
        #print(SoC_data_string)
        SoC_data_position= SoC_data_string.find("0xc4,")
        SoC_data_position_start = SoC_data_position+6

        if SoC_data_string.find("0xc4,") != -1:
            #find position whereafter the important data will be given
#                 print ("message")
            #start filtering with 4 possibilities
            if SoC_data_string[SoC_data_position_start+3]==",":  #pre-possibility 0x0,
                SoC_data_position_1_end = SoC_data_position_start+3
                SoC_data_HEX_1 = SoC_data_string[SoC_data_position_start:SoC_data_position_1_end]
                
                if SoC_data_string[SoC_data_position_start+8]==",": #possibility 1: 0x0, 0x0,
                    SoC_data_position_2_end = SoC_data_position_start+7
                    SoC_data_HEX_2 = SoC_data_string[SoC_data_position_2_end]
                else: #possibility 2: 0x0, 0x00,
                    SoC_data_position_2_start = SoC_data_position_start+7
                    SoC_data_position_2_end = SoC_data_position_start+9
                    SoC_data_HEX_2 = SoC_data_string[SoC_data_position_2_start:SoC_data_position_2_end]
                
            else: #pre-possibility 0x00,
                if SoC_data_string[SoC_data_position_start+9]==",": #possibility 3: 0x00, 0x0,
                    SoC_data_position_1_end = SoC_data_position_start+4
                    SoC_data_HEX_1 = SoC_data_string[SoC_data_position_start:SoC_data_position_1_end]
                    SoC_data_position_2_end = SoC_data_position_start+8
                    SoC_data_HEX_2 = SoC_data_string[SoC_data_position_2_end]
                else: #possibility 4: 0x00, 0x00,        
                    SoC_data_position_1_end = SoC_data_position_start+4
                    SoC_data_HEX_1 = SoC_data_string[SoC_data_position_start:SoC_data_position_1_end]
                    SoC_data_position_2_start = SoC_data_position_start+8
                    SoC_data_position_2_end = SoC_data_position_start+10
                    SoC_data_HEX_2 = SoC_data_string[SoC_data_position_2_start:SoC_data_position_2_end]
            SoC_data_HEX = SoC_data_HEX_1 + SoC_data_HEX_2
            #convert HEX-Code to integer-value with base 16 for HEX-values and multiply by 0.01
            SoC_data_real=int(SoC_data_HEX,16)*0.01 #the real value based on max battery capacity
            SoC_data = SoC_data_real*1.294-10.6 #displayed and usable charge
            #print("SoC_data: ")
            #print(SoC_data)
        else:
            SoC_data = 0
        
#         #___________________________SoH__________________________________
#         
#         self.getCanPort().send(self.getMessageSoH())
#         # response should be can_id=0x607, data=[0xF1, 0x04, 0x62, 0xDD, 0x7b, 0xdata1]
# #             print("SoH Message sent")
#         
#         # filter unnecessary codes from other buses, but can't fully filter because the can-library can't fully do it
#         self.getCanPort().set_filters([{"can_id":0x607, "can_mask":0xF1, "extended":False}]) 
#         SoH_all_data = self.getCanPort().recv()
# #             print(SoH_all_data)
# 
#         #______prepare for manual filtering______
#         #create an array, then string for filtering
#         SoH_data_array=np.array([SoH_all_data])
#         SoH_data_string= str(SoH_data_array)
# 
#         #find position whereafter the important data will be given
#         SoH_data_position= SoH_data_string.find("0x7b")
#         SoH_data_position_start = SoH_data_position+6
#         
#         if SoH_data_string.find("0x7b,") != -1:
#             #find position whereafter the important data will be given
# #                 print ("message")
#             #start filtering with 2 possibilities
#             if SoH_data_string[SoH_data_position_start+3]=="]":  #possibility 1: 0x0,
#                 SoH_data_position_end = SoH_data_position_start+3
#                 SoH_data_HEX = SoH_data_string[SoH_data_position_start:SoH_data_position_end]
# 
#             else: #possibility 2: 0x00,
#                 SoH_data_position_end = SoH_data_position_start+4
#                 SoH_data_HEX = SoH_data_string[SoH_data_position_start:SoH_data_position_end]
# 
#             #convert HEX-Code to integer-value with base 16 for HEX-values
#             SoH_data=int(SoH_data_HEX,16)
#         
#         else:
#             SoH_data = 0

              
        self.dataStr = "{:8.6f}, {:8.6f}".format(SoC_data, 0)  # ???
                
        #except:
         #   print ("No connection to the eCar!")
            
    def getData(self):
        return self.dataStr