from os import TMP_MAX
from sys import byteorder
import canopen
#import cantools
import time
import CircularBuffer
from numpy import loadtxt
from MLModel import MLModel
import time
import threading
num_rpdo = 18

# construct a CAN network
network = canopen.Network()

# connect to the CAN network
#network.connect(bustype='socketcan', channel='vcan0', bitrate=1000000)
network.connect(bustype='socketcan', channel='can0', bitrate=1000000)

# create a slaver node with id 2(need to match with master.py) and Object Dictionary "Slaver.eds"
Jetson_66 = network.create_node(66, 'Jetson_66_v12.eds')

# Node send the boot-up message to the CAN network COB-ID:0x700+node-ID detail: "0"
Jetson_66.nmt.send_command(0)

# With the heartbeat configuration in object Dictionary, use the function by following command every 1s(1000ms)
Jetson_66.nmt.start_heartbeat(1000)  

# send pdo message
Jetson_66.rpdo.read()
Jetson_66.tpdo.read()

print("CAN BUS configuration completed, waiting RPDO...")

    
Left_unsigned16bit_raw = [0]*12
Right_unsigned16bit_raw = [0]*12
Left_crutch_data = [0]*6
Right_crutch_data = [0]*6
isPDOreceived = [0]*12
startTime = time.perf_counter()


def process_rpdo(message): # "message" type: 'canopen.pdo.base.Map'; var type: 'canopen.pdo.base.Variable'  
    # print('%s received' % message.name)
    cob_id = str(hex(message.cob_id))
    # Add crutch sensor pdo criteria by message.cob_id

    # (message.arbitration_id, message.data) 'Map' object has no attribute 'arbitration_id' ???
    splited_hex = [0]*int((len(message)))
    i = 0
    global isPDOreceived
    global LH_position
    global LK_position
    global RH_position
    global RK_position
    global LH_velocity
    global LK_velocity
    global RH_velocity
    global RK_velocity
    global LH_torque
    global LK_torque
    global RH_torque
    global RK_torque

    for var in message:
        splited_hex[i] = var.raw
        i = i+1
        # print('%s = %d' % (var.name, var.raw)) # var.name = str; var.raw = int(Raw representation of the object.)
        # print(type(splited_hex[0]))
    # Left Hip Motor   
    if cob_id[2:5] == '281': # if rpdo is 0x2-- , split msg into position and velocity
        # split list > create bytes class > convert bytes to int in little-endian
        LH_position = int.from_bytes(bytes(splited_hex[0:4]), byteorder='little', signed=True) 
        LH_velocity = int.from_bytes(bytes(splited_hex[4:8]), byteorder='little', signed=True)
        # print("LH_position =", LH_position, "LH_velocity =", LH_velocity )
        isPDOreceived[0] = 1
    elif cob_id[2:5] == '381': # if rpdo is 0x3--, set denominator to 1 to extract all msg as torque
        LH_torque = int.from_bytes(bytes(splited_hex), byteorder='little', signed=True)
        # print("LH_torque =", LH_torque)
        isPDOreceived[1] = 1
    # Left Knee Motor
    elif cob_id[2:5] == '282':
        LK_position = int.from_bytes(bytes(splited_hex[0:4]), byteorder='little', signed=True) 
        LK_velocity = int.from_bytes(bytes(splited_hex[4:8]), byteorder='little', signed=True)
        # print("LK_position =", LK_position, "LK_velocity =", LK_velocity )
        isPDOreceived[2] = 1
    elif cob_id[2:5] == '382':
        LK_torque = int.from_bytes(bytes(splited_hex), byteorder='little', signed=True)
        # print("LK_torque =", LK_torque)
        isPDOreceived[3] = 1
    # Right Hip Motor
    elif cob_id[2:5] == '283':
        RH_position = int.from_bytes(bytes(splited_hex[0:4]), byteorder='little', signed=True) 
        RH_velocity = int.from_bytes(bytes(splited_hex[4:8]), byteorder='little', signed=True)
        # print("RH_position =", RH_position, "RH_velocity =", RH_velocity )
        isPDOreceived[4] = 1
    elif cob_id[2:5] == '383':
        RH_torque = int.from_bytes(bytes(splited_hex), byteorder='little', signed=True)
        # print("RH_torque =", RH_torque)
        isPDOreceived[5] = 1
    # Right Knee Motor
    elif cob_id[2:5] == '284':
        RK_position = int.from_bytes(bytes(splited_hex[0:4]), byteorder='little', signed=True) 
        RK_velocity = int.from_bytes(bytes(splited_hex[4:8]), byteorder='little', signed=True)
        # print("RK_position =", RK_position, "RK_velocity =", RK_velocity )
        isPDOreceived[6] = 1
    elif cob_id[2:5] == '384':
        RK_torque = int.from_bytes(bytes(splited_hex), byteorder='little', signed=True)
        # print("RK_torque =", RK_torque)
        isPDOreceived[7] = 1

    # Config crutch sensor data convertion
    elif cob_id[2:4] == 'f1':
        for i in range(7):
            Left_unsigned16bit_raw[i] = splited_hex[i+1]
        isPDOreceived[8] = 1
    elif cob_id[2:4] == 'f9':
        for i in range(7):
            Right_unsigned16bit_raw[i] = splited_hex[i+1]
        isPDOreceived[9] = 1
    elif cob_id[2:4] == 'f2':
        for i in range(5):
            Left_unsigned16bit_raw[i+7] = splited_hex[i]
        # print("Left_unsigned16bit_raw",Left_unsigned16bit_raw)
        for i in range(0,6):
            Left_crutch_data[i] = int.from_bytes(bytes(Left_unsigned16bit_raw[0+2*i:2+2*i]), byteorder='big', signed=True)
            Left_crutch_data[i] = Left_crutch_data[i] - 2^16
            if(i<3):
                Left_crutch_data[i] = Left_crutch_data[i]/50
            elif(i>=3):
                Left_crutch_data[i] = Left_crutch_data[i]/2000
        isPDOreceived[10] = 1
        # print("Left_crutch_data",Left_crutch_data)
    elif cob_id[2:4] == 'fa':
        for i in range(5):
            Right_unsigned16bit_raw[i+7] = splited_hex[i]
        # print("Right_unsigned16bit_raw",Right_unsigned16bit_raw)
        for i in range(0,6):
            Right_crutch_data[i] = int.from_bytes(bytes(Right_unsigned16bit_raw[0+2*i:2+2*i]), byteorder='big', signed=True)
            Right_crutch_data[i] = Right_crutch_data[i] - 2^16
            if(i<3):
                Right_crutch_data[i] = Right_crutch_data[i]/50
            elif(i>=3):
                Right_crutch_data[i] = Right_crutch_data[i]/2000
        isPDOreceived[11] = 1
        # print("Right_crutch_data",Right_crutch_data)

    if(isPDOreceived[0]==1 and isPDOreceived[1]==1 and isPDOreceived[2]==1 and isPDOreceived[3]==1 and isPDOreceived[4]==1
     and isPDOreceived[5]==1 and isPDOreceived[6]==1 and isPDOreceived[7]==1 and isPDOreceived[8]==1 and isPDOreceived[9]==1
     and isPDOreceived[10]==1 and isPDOreceived[11]==1):
        for i in range(6):
            model_input_circular.append(Left_crutch_data[i])
        for i in range(6):
            model_input_circular.append(Right_crutch_data[i])
        model_input_circular.append(LH_position)
        model_input_circular.append(LK_position)
        model_input_circular.append(RH_position)
        model_input_circular.append(RK_position)
        model_input_circular.append(LH_velocity)
        model_input_circular.append(LK_velocity)
        model_input_circular.append(RH_velocity)
        model_input_circular.append(RK_velocity)
        model_input_circular.append(LH_torque)
        model_input_circular.append(LK_torque)
        model_input_circular.append(RH_torque)
        model_input_circular.append(RK_torque)
        isPDOreceived = [0]*12
        print("model_input_circular actual size=", model_input_circular.ActualSize)
        timediff = time.perf_counter() - startTime
        print(f"eElapsed time since last buffer fill {timediff:0.4f} s")



#Create the intent prediction dictionary
intents = {
    "walk~fwd": 0,
    "walkFL~stand": 1
}


#Create the ML model
myMLModel = MLModel('walk_L_ML_model.joblib','walk_L_PCA.joblib',intents)



# print("isPDOreceived",isPDOreceived)
model_input_circular  = CircularBuffer.circularlist(2400)

for i in range(1,num_rpdo):
    Jetson_66.rpdo[i].add_callback(process_rpdo)

while(True):
    #Perform Prediction using ML model and Exo data
    #print([model_input_circular.Data])
    if model_input_circular.ActualSize == 2400:
        prediction = myMLModel.make_prediction([model_input_circular.Data])
        print('The Prediction is:')
        print(prediction)
    
