# from Jetson.CallbackTest.Jetson_rpdo import LH_torque, Left_crutch_data
from ast import Global
import canopen
import time
from abc import abstractmethod
from interface.Network import Network
from Converter import Converter
import CircularBuffer
from enum import IntEnum

class DataOrder(IntEnum):
    L_CRUTCH = 0 #crutch has 6 data each
    R_CRUTCH = 6 #crutch has 6 data each
    LH_position = 12
    LK_position = 13
    RH_position = 14
    RK_position = 15
    LH_velocity = 16
    LK_velocity = 17
    RH_velocity = 18
    RK_velocity = 19 
    LH_torque = 20
    LK_torque = 21
    RH_torque = 22
    RK_torque = 23

numData = 24

class CANNetwork(Network):
	## CAN network implementation 
	# Processes PDO and puts relevant data into circularBuffer for the ML model to use
    # CircularBuffer is updated when the update function is called. 
    # The calling of the update function should occur outside of the class using RepeatTimerThread
    def __init__(self, nodeid, num_rpdo, edsfileName, circularBuffer):
        self.network = None
        self.node = None
        self.nodeid = int(nodeid)
        self.num_rpdo = num_rpdo
        self.edsfileName = edsfileName
        self.isPDOreceived = [0]*12
        self.num_pdo_received = [0]*13
        self.model_input_circular  = circularBuffer
        self.Left_unsigned16bit_raw = [0]*12
        self.Right_unsigned16bit_raw = [0]*12
        self.tempbuffer = [0] * numData
        self.startTime = 0
        self.rpdo_converter = Converter()
        self.current_state = 0
        self.acceptPrediction = True
        self.numPdo = 0
        
    
    def Setup(self):
    ## Setup the connection object
    # construct a CAN network
        self.network = canopen.Network()

        # connect to the CAN network
        #self.network.connect(bustype='socketcan', channel='vcan0', bitrate=1000000)
        self.network.connect(bustype='socketcan', channel='can0', bitrate=1000000)

        # create a slaver node with id 2(need to match with master.py) and Object Dictionary "Slaver.eds"
        self.node = self.network.create_node(self.nodeid , self.edsfileName )

        # Node send the boot-up message to the CAN network COB-ID:0x700+node-ID detail: "0"
        self.node.nmt.send_command(0)

        # With the heartbeat configuration in object Dictionary, use the function by following command every 1s(1000ms)
        self.node.nmt.start_heartbeat(1000)  

        # send pdo message
        self.node.rpdo.read()
        self.node.tpdo.read()
        #add callbacks
        for i in range(1, self.num_rpdo):
            self.node.rpdo[i].add_callback(self.process_rpdo)     
    
    def Update(self): 
    ## Any polling goes here 
        for i in range(numData):
            self.model_input_circular.append(self.tempbuffer[i]) 
        #print(self.tempbuffer)

    def SetupHardware(self):
        print(self.num_pdo_received)
    ## For setting up hardware (might not be in use

    
    def process_rpdo(self,message): # "message" type: 'canopen.pdo.base.Map'; var type: 'canopen.pdo.base.Variable'  
        # print('%s received' % message.name)
        cob_id = str(hex(message.cob_id))
        #self.numPdo += 1
        # Add crutch sensor pdo criteria by message.cob_id
        splited_hex = [var.raw for var in message]
        #print(cob_id[2:5], len(self.tempbuffer))
        if cob_id[2:5] == '281': # if rpdo is 0x2-- , split msg into position and velocity
            # split list > create bytes class > convert bytes to int in little-endian
            self.tempbuffer[DataOrder.LH_position] = self.rpdo_converter.position(splited_hex)
            self.tempbuffer[DataOrder.LH_velocity] = self.rpdo_converter.velocity(splited_hex)
            self.isPDOreceived[0] = 1
            self.num_pdo_received[0] += 1
        elif cob_id[2:5] == '381': # if rpdo is 0x3--, set denominator to 1 to extract all msg as torque
            self.tempbuffer[DataOrder.LH_torque] = self.rpdo_converter.torque(splited_hex)
            #print(splited_hex)
            self.isPDOreceived[1] = 1
            self.num_pdo_received[1] += 1
        # Left Knee Motor
        elif cob_id[2:5] == '282':
            self.tempbuffer[DataOrder.LK_position] = self.rpdo_converter.position(splited_hex)
            self.tempbuffer[DataOrder.LK_velocity] = self.rpdo_converter.velocity(splited_hex)
            self.isPDOreceived[2] = 1
            self.num_pdo_received[2] += 1
        elif cob_id[2:5] == '382':
            #print(splited_hex)
            self.tempbuffer[DataOrder.LK_torque] = self.rpdo_converter.torque(splited_hex)
            self.isPDOreceived[3] = 1
            self.num_pdo_received[3] += 1
        # Right Hip Motor
        elif cob_id[2:5] == '283':
            self.tempbuffer[DataOrder.RH_position] = self.rpdo_converter.position(splited_hex)
            self.tempbuffer[DataOrder.RH_velocity] = self.rpdo_converter.velocity(splited_hex)
            self.isPDOreceived[4] = 1
            self.num_pdo_received[4] += 1
        elif cob_id[2:5] == '383':
            #print(splited_hex)
            self.tempbuffer[DataOrder.RH_torque] = self.rpdo_converter.torque(splited_hex)
            
            self.isPDOreceived[5] = 1
            self.num_pdo_received[5] += 1
        # Right Knee Motor
        elif cob_id[2:5] == '284':
            self.tempbuffer[DataOrder.RK_position] = self.rpdo_converter.position(splited_hex)
            self.tempbuffer[DataOrder.RK_velocity] = self.rpdo_converter.velocity(splited_hex)
            self.isPDOreceived[6] = 1
            self.num_pdo_received[6] += 1
        elif cob_id[2:5] == '384':
            #print(splited_hex)
            self.tempbuffer[DataOrder.RK_torque] = self.rpdo_converter.torque(splited_hex)
            self.isPDOreceived[7] = 1
            self.num_pdo_received[7] += 1
        # Config crutch sensor data convertion
        elif cob_id[2:4] == 'f1':
            self.Left_unsigned16bit_raw = self.rpdo_converter.Left_crutch_data_1(splited_hex)
            self.isPDOreceived[8] = 1
            self.num_pdo_received[8] += 1
        elif cob_id[2:4] == 'f9':
            self.Right_unsigned16bit_raw = self.rpdo_converter.Right_crutch_data_1(splited_hex)
            #print(self.Right_unsigned16bit_raw)
            self.isPDOreceived[9] = 1
            self.num_pdo_received[9] += 1
        elif cob_id[2:4] == 'f2':
            self.num_pdo_received[10] += 1
            if self.isPDOreceived[8] == 1:
                self.tempbuffer[DataOrder.L_CRUTCH: DataOrder.L_CRUTCH+6] = \
                     self.rpdo_converter.Left_crutch_data_2(self.Left_unsigned16bit_raw, splited_hex)
                self.isPDOreceived[10] = 1
           # print("Left_crutch_data",Left_crutch_data)
        elif cob_id[2:4] == 'fa':
            self.num_pdo_received[11] += 1
            #print(len(self.tempbuffer))
            if self.isPDOreceived[9] == 1:
                self.tempbuffer[DataOrder.R_CRUTCH: DataOrder.R_CRUTCH+6] = \
                    self.rpdo_converter.Right_crutch_data_2(self.Right_unsigned16bit_raw, splited_hex)
                self.isPDOreceived[11] = 1
            #print(self.tempbuffer[DataOrder.R_CRUTCH: DataOrder.R_CRUTCH+6])

            #print(self.tempbuffer[DataOrder.R_CRUTCH: DataOrder.R_CRUTCH+6])
        elif cob_id[2:5] == '211': # if rpdo is 0x211, storage the current state
            self.num_pdo_received[12] += 1
            self.current_state = splited_hex[0]
            #print("Current state:",self.current_state)
        elif cob_id[2:5] == "194": #this sets if prediction is enabled
            self.acceptPrediction = bool(splited_hex[0])
            #print("Accept prediction:",self.acceptPrediction)
        #else: 
            #print("Invalid COB-ID", cob_id) 
            

    def transmit_prediction(self, prediction):
        # print('prediction: ', prediction)
        if prediction != 'invalid':
            self.node.tpdo[1][0x2000].raw = prediction
            self.node.tpdo[1].transmit()
    
