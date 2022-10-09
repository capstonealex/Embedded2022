# from Jetson.CallbackTest.Jetson_rpdo import LH_torque, Left_crutch_data
from ast import Global
import canopen
import time
from .Converter import Converter
from .Network import Network
from ..AlexStates import AlexState
from enum import IntEnum
from os import path

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



class CANNetwork(Network):
    """!CAN network implementation: reads and processes CAN messages 
	
    Processes PDO and puts relevant data into circularBuffer.
    CircularBuffer is updated when the update function is called. 
    Keeps track of the state of the exoskeleton and crutch.
    """
    def __init__(self, nodeid:int, num_rpdo:int, eds_filename:str, 
                circular_buffer, virtual_can:bool = False):
        """!Initalizes the CANNetwork class

        Args:
            nodeid (int): the node id on the CAN network
            num_rpdo (int): Number of rpdos in eds file
            eds_filename (str): path of the eds file
            circular_buffer (CircularBuffer): Data structure to share data on
            virtual_can (bool) : Use virtual CAN bus if true, defaults to false
        """
        self._network = None
        self._node = None
        self._nodeid = int(nodeid)
        self._num_rpdo = num_rpdo
        self._edsfileName = path.join(path.dirname(path.realpath(__file__)), eds_filename)
        self._isPDOreceived = [0]*12
        self._num_pdo_received = [0]*13
        self._model_input_circular  = circular_buffer
        self._left_unsigned16bit_raw = [0]*12
        self._right_unsigned16bit_raw = [0]*12
        self._tempbuffer = [0] * 24
        self._startTime = 0
        self.rpdo_converter = Converter()
        self.current_state = 0
        self._virtual = virtual_can
        self.accept_prediction = True
        
    
    def Setup(self):
        """ !Setup the connection, connect to CAN network
        """
        
        self._network = canopen.Network()

        # connect to the CAN network
        if self._virtual:
            self._network.connect(bustype='socketcan', channel='vcan0', bitrate=1000000)
        else:
            self._network.connect(bustype='socketcan', channel='can0', bitrate=1000000)

        # create a slaver node with id 2(need to match with master.py) and Object Dictionary "Slaver.eds"
        self._node = self._network.create_node(self._nodeid , self._edsfileName )

        # Node send the boot-up message to the CAN network COB-ID:0x700+node-ID detail: "0"
        self._node.nmt.send_command(0)

        # With the heartbeat configuration in object Dictionary, use the function by following command every 1s(1000ms)
        self._node.nmt.start_heartbeat(1000)  

        # send pdo message
        self._node.rpdo.read()
        self._node.tpdo.read()
        #add callbacks
        for i in range(1, self._num_rpdo):
            self._node.rpdo[i].add_callback(self.process_rpdo)     
    
    def Update(self): 
    ## Any polling goes here 
        for i in range(24):
            self._model_input_circular.append(self._tempbuffer[i]) 
        #print(self.tempbuffer)

    def SetupHardware(self):
        print(self._num_pdo_received)
    ## For setting up hardware (might not be in use

    
    def process_rpdo(self,message): 
        """Callback function to process various rpdos 

        Args:
            message (canopen.pdo.base.Map)
        """ 
        
        cob_id = str(hex(message.cob_id))
        # Add crutch sensor pdo criteria by message.cob_id
        splited_hex = [var.raw for var in message]
        #print(cob_id[2:5], len(self.tempbuffer))
        if cob_id[2:5] == '281': # if rpdo is 0x2-- , split msg into position and velocity
            # split list > create bytes class > convert bytes to int in little-endian
            self._tempbuffer[DataOrder.LH_position] = self.rpdo_converter.position(splited_hex)
            self._tempbuffer[DataOrder.LH_velocity] = self.rpdo_converter.velocity(splited_hex)
            self._isPDOreceived[0] = 1
            self._num_pdo_received[0] += 1
        elif cob_id[2:5] == '381': # if rpdo is 0x3--, set denominator to 1 to extract all msg as torque
            self._tempbuffer[DataOrder.LH_torque] = self.rpdo_converter.torque(splited_hex)
            #print(splited_hex)
            self._isPDOreceived[1] = 1
            self._num_pdo_received[1] += 1
        # Left Knee Motor
        elif cob_id[2:5] == '282':
            self._tempbuffer[DataOrder.LK_position] = self.rpdo_converter.position(splited_hex)
            self._tempbuffer[DataOrder.LK_velocity] = self.rpdo_converter.velocity(splited_hex)
            self._isPDOreceived[2] = 1
            self._num_pdo_received[2] += 1
        elif cob_id[2:5] == '382':
            #print(splited_hex)
            self._tempbuffer[DataOrder.LK_torque] = self.rpdo_converter.torque(splited_hex)
            self._isPDOreceived[3] = 1
            self._num_pdo_received[3] += 1
        # Right Hip Motor
        elif cob_id[2:5] == '283':
            self._tempbuffer[DataOrder.RH_position] = self.rpdo_converter.position(splited_hex)
            self._tempbuffer[DataOrder.RH_velocity] = self.rpdo_converter.velocity(splited_hex)
            self._isPDOreceived[4] = 1
            self._num_pdo_received[4] += 1
        elif cob_id[2:5] == '383':
            #print(splited_hex)
            self._tempbuffer[DataOrder.RH_torque] = self.rpdo_converter.torque(splited_hex)
            
            self._isPDOreceived[5] = 1
            self._num_pdo_received[5] += 1
        # Right Knee Motor
        elif cob_id[2:5] == '284':
            self._tempbuffer[DataOrder.RK_position] = self.rpdo_converter.position(splited_hex)
            self._tempbuffer[DataOrder.RK_velocity] = self.rpdo_converter.velocity(splited_hex)
            self._isPDOreceived[6] = 1
            self._num_pdo_received[6] += 1
        elif cob_id[2:5] == '384':
            #print(splited_hex)
            self._tempbuffer[DataOrder.RK_torque] = self.rpdo_converter.torque(splited_hex)
            self._isPDOreceived[7] = 1
            self._num_pdo_received[7] += 1
        # Config crutch sensor data convertion
        elif cob_id[2:4] == 'f1':
            self._left_unsigned16bit_raw = self.rpdo_converter.Left_crutch_data_1(splited_hex)
            self._isPDOreceived[8] = 1
            self._num_pdo_received[8] += 1
        elif cob_id[2:4] == 'f9':
            self._right_unsigned16bit_raw = self.rpdo_converter.Right_crutch_data_1(splited_hex)
            #print(self.Right_unsigned16bit_raw)
            self._isPDOreceived[9] = 1
            self._num_pdo_received[9] += 1
        elif cob_id[2:4] == 'f2':
            self._num_pdo_received[10] += 1
            if self._isPDOreceived[8] == 1:
                self._tempbuffer[DataOrder.L_CRUTCH: DataOrder.L_CRUTCH+6] = \
                     self.rpdo_converter.Left_crutch_data_2(self._left_unsigned16bit_raw, splited_hex)
                self._isPDOreceived[10] = 1
           # print("Left_crutch_data",Left_crutch_data)
        elif cob_id[2:4] == 'fa':
            self._num_pdo_received[11] += 1
            #print(len(self.tempbuffer))
            if self._isPDOreceived[9] == 1:
                self._tempbuffer[DataOrder.R_CRUTCH: DataOrder.R_CRUTCH+6] = \
                    self.rpdo_converter.Right_crutch_data_2(self._right_unsigned16bit_raw, splited_hex)
                self._isPDOreceived[11] = 1
            #print(self.tempbuffer[DataOrder.R_CRUTCH: DataOrder.R_CRUTCH+6])

            #print(self.tempbuffer[DataOrder.R_CRUTCH: DataOrder.R_CRUTCH+6])
        elif cob_id[2:5] == '211': # if rpdo is 0x211, storage the current state
            self._num_pdo_received[12] += 1
            self.current_state = splited_hex[0]
            print("The current state is:" ,AlexState(self.current_state))
            #print("Current state:",self.current_state)
        elif cob_id[2:5] == "194": #this sets if prediction is enabled
            self.accept_prediction = bool(splited_hex[0])
            #print("Accept prediction:",self.acceptPrediction)
        #else: 
            #print("Invalid COB-ID", cob_id) 
            

    def transmit_prediction(self, prediction):
        # print('prediction: ', prediction)
        if prediction != 'invalid':
            self._node.tpdo[1][0x2000].raw = prediction
            self._node.tpdo[1].transmit()
    
    def Update(self): 
        for i in range(24):
            self._model_input_circular.append(self._tempbuffer[i]) 
