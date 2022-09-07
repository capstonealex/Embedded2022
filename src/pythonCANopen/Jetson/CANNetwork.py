from Jetson.CallbackTest.Jetson_rpdo import LH_torque, Left_crutch_data
import canopen
import time
from abc import abstractmethod
from interface.Network import Network
from Converter import Converter
import CircularBuffer

class CANNetwork(Network):
	## CAN network implementation 
	# 
    def __init__(self, nodeid, num_rpdo, edsfileName):
        self.network = None
        self.node = None
        self.nodeid = int(nodeid)
        self.num_rpdo = num_rpdo
        self.edsfileName = edsfileName
        self.isPDOreceived = [0]*12
        self.model_input_circular  = CircularBuffer.circularlist(24)
    
    def Setup(self):
    ## Setup the connection object
    # construct a CAN network
        self.network = canopen.Network()

        # connect to the CAN network
        self.network.connect(bustype='socketcan', channel='vcan0', bitrate=1000000)
        # self.network.connect(bustype='socketcan', channel='can0', bitrate=1000000)

        # create a slaver node with id 2(need to match with master.py) and Object Dictionary "Slaver.eds"
        self.node = self.network.create_node(self.nodeid , self.edsfileName )

        # Node send the boot-up message to the CAN network COB-ID:0x700+node-ID detail: "0"
        self.node.nmt.send_command(0)

        # With the heartbeat configuration in object Dictionary, use the function by following command every 1s(1000ms)
        self.node.nmt.start_heartbeat(1000)  

        # send pdo message
        self.node.rpdo.read()
        self.node.tpdo.read()

    def process_rpdo(self,message): # "message" type: 'canopen.pdo.base.Map'; var type: 'canopen.pdo.base.Variable'  
        # print('%s received' % message.name)
        cob_id = str(hex(message.cob_id))
        # Add crutch sensor pdo criteria by message.cob_id

        # (message.arbitration_id, message.data) 'Map' object has no attribute 'arbitration_id' ???Leftself.
        splited_hex = [0]*int((len(message)))
        i = 0
        for var in message:
            splited_hex[i] = var.raw
            i = i+1
            # print('%s = %d' % (var.name, var.raw)) # var.name = str; var.raw = int(Raw representation of the object.)
            # print(type(splited_hex[0]))
        rpdo_converter = Converter()

        # Left Hip Motor   
        if cob_id[2:5] == '281': # if rpdo is 0x2-- , split msg into position and velocity
            # split list > create bytes class > convert bytes to int in little-endian
            LH_position = rpdo_converter.position(splited_hex)
            LH_velocity = rpdo_converter.velocity(splited_hex)
            self.isPDOreceived[0] = 1
        elif cob_id[2:5] == '381': # if rpdo is 0x3--, set denominator to 1 to extract all msg as torque
            LH_torque = rpdo_converter.torque(splited_hex)
            self.isPDOreceived[1] = 1
        # Left Knee Motor
        elif cob_id[2:5] == '282':
            LK_position = rpdo_converter.position(splited_hex)
            LK_velocity = rpdo_converter.velocity(splited_hex)
            self.isPDOreceived[2] = 1
        elif cob_id[2:5] == '382':
            LK_torque = rpdo_converter.torque(splited_hex)
            self.isPDOreceived[3] = 1
        # Right Hip Motor
        elif cob_id[2:5] == '283':
            RH_position = rpdo_converter.position(splited_hex)
            RH_velocity = rpdo_converter.velocity(splited_hex)
            self.isPDOreceived[4] = 1
        elif cob_id[2:5] == '383':
            RH_torque = rpdo_converter.torque(splited_hex)
            self.isPDOreceived[5] = 1
        # Right Knee Motor
        elif cob_id[2:5] == '284':
            RK_position = rpdo_converter.position(splited_hex)
            RK_velocity = rpdo_converter.velocity(splited_hex)
            self.isPDOreceived[6] = 1
        elif cob_id[2:5] == '384':
            RK_torque = rpdo_converter.torque(splited_hex)
            self.isPDOreceived[7] = 1

        # Config crutch sensor data convertion
        elif cob_id[2:4] == 'f1':
            Left_unsigned16bit_raw = rpdo_converter.Left_crutch_data_1(splited_hex)
            self.isPDOreceived[8] = 1
        elif cob_id[2:4] == 'f9':
            Right_unsigned16bit_raw = rpdo_converter.Right_crutch_data_1(splited_hex)
            self.isPDOreceived[9] = 1
        elif cob_id[2:4] == 'f2':
            Left_crutch_data = rpdo_converter.Left_crutch_data_2(Left_unsigned16bit_raw, splited_hex)
            self.isPDOreceived[10] = 1
            # print("Left_crutch_data",Left_crutch_data)
        elif cob_id[2:4] == 'fa':
            Right_crutch_data = rpdo_converter.Right_crutch_data_2(Right_unsigned16bit_raw, splited_hex)
            self.isPDOreceived[11] = 1
            # print("Right_crutch_data",Right_crutch_data)

        if(self.isPDOreceived[0]==1 and self.isPDOreceived[1]==1 and self.isPDOreceived[2]==1 and self.isPDOreceived[3]==1 and self.isPDOreceived[4]==1
        and self.isPDOreceived[5]==1 and self.isPDOreceived[6]==1 and self.isPDOreceived[7]==1 and self.isPDOreceived[8]==1 and self.isPDOreceived[9]==1
        and self.isPDOreceived[10]==1 and self.isPDOreceived[11]==1):
            for i in range(6):
                self.model_input_circular.append(Left_crutch_data[i])
            for i in range(6):
                self.model_input_circular.append(Right_crutch_data[i])
            self.model_input_circular.append(LH_position)
            self.model_input_circular.append(LK_position)
            self.model_input_circular.append(RH_position)
            self.model_input_circular.append(RK_position)
            self.model_input_circular.append(LH_velocity)
            self.model_input_circular.append(LK_velocity)
            self.model_input_circular.append(RH_velocity)
            self.model_input_circular.append(RK_velocity)
            self.model_input_circular.append(LH_torque)
            self.model_input_circular.append(LK_torque)
            self.model_input_circular.append(RH_torque)
            self.model_input_circular.append(RK_torque)
            self.isPDOreceived = [0]*12
            print("model_input_circular=", self.model_input_circular)

    def Update(self): 
    ## Any polling goes here 
        for i in range(1,self.num_rpdo):
            self.node.rpdo[i].add_callback(self.process_rpdo)

    def SetupHardware(self):
    ## For setting up hardware (might not be in use
        pass