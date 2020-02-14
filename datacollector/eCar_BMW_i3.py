#e-Car read CAN
#python program to read out CAN-Data over OBD-II
#version 0.1
#University of applied science Karlsruhe (HsKa)
#etaNet: Management strategy for a CHP with heat storage, consumer and electric vehicle
#in the field of cyberphysical Systems
#WiSe 2019/2020
#Vitali Müller
#Ferhat Aslan

# following code is implemented in /etc/rc.local (autostart) for communication with the PiCAN2 RPI shield after booting
# /sbin/ip link set can0 up type can bitrate 500000


#=======================imports==============================#

import can
import time
import numpy as np

#=======================initial settings==============================#

bus = can.interface.Bus(channel='can0', bustype='socketcan_native')#, bitrate=500000)

#=======================functions==============================#
  
def SoC_value():
    SoC = can.Message(arbitration_id=0x6F1,
                      data=[0x07, 0x03, 0x22, 0xDD, 0xC4, 0x00, 0x00, 0x00],
                      extended_id=False)

    while True:
        bus.send(SoC)
        print("SoC Message sent")
        
        # filter unnecessary codes from other buses, but can't fully filter because the can-library can't fully do it
        bus.set_filters([{"can_id":0x607, "can_mask":0xF1, "extended":False}]) 
        SoC_all_data = bus.recv()
        
        #______prepare for manual filtering______
        #create an array, then string for filtering
        SoC_data_array=np.array([SoC_all_data])
        SoC_data_string= str(SoC_data_array)
        
        #find position whereafter the important data will be given
        SoC_data_position= SoC_data_string.find("0xc4,")
        SoC_data_position_start = SoC_data_position+6
        
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

        #combine the strings together, from e.g. 0x00, 0x00, to 0x0000
        SoC_data_HEX = SoC_data_HEX_1 + SoC_data_HEX_2
        #convert HEX-Code to integer-value with base 16 for HEX-values and multiply by 0.01
        SoC_data=int(SoC_data_HEX,16)*0.01
        #print(SoC_data)
        return SoC_data
    
    else:
        print("error")
        
        
def SoH_value():
    SoH = can.Message(arbitration_id=0x6F1,
                      data=[0x07, 0x03, 0x22, 0xDD, 0x7B, 0x00, 0x00, 0x00],
                      extended_id=False)

    while True:
        bus.send(SoH)
        print("SoH Message sent")
        
        # filter unnecessary codes from other buses, but can't fully filter because the can-library can't fully do it
        bus.set_filters([{"can_id":0x607, "can_mask":0xF1, "extended":False}]) 
        SoH_data = bus.recv()
        
        #______prepare for manual filtering______
        #create an array, then string for filtering
        SoH_data_array=np.array([y])
        SoH_data_string= str(SoH_data_array)

        #find position whereafter the important data will be given
        SoH_data_position= SoH_data_string.find("0x7b")
        SoH_data_position_start = SoH_data_position+6
        
        #start filtering with 2 possibilities
        if SoH_data_string[SoH_data_position_start+3]=="]":  #possibility 1: 0x0,
            SoH_data_position_end = SoH_data_position_start+3
            SoH_data_HEX = SoH_data_string[SoH_data_position_start:SoH_data_position_end]

        else: #possibility 2: 0x00,
            SoH_data_position_end = SoH_data_position_start+4
            SoH_data_HEX = SoH_data_string[SoH_data_position_start:SoH_data_position_end]

        print(SoH_data_HEX)
        #convert HEX-Code to integer-value with base 16 for HEX-values
        SoH_data=int(SoH_data_HEX,16)
        print(SoH_data)

        return SoH_data
    else:
        print("error")
