from os import TMP_MAX
from sys import byteorder
import canopen
import cantools
import time
import CircularBuffer

num_rpdo = 18

# construct a CAN network
network = canopen.Network()

# connect to the CAN network
network.connect(bustype='socketcan', channel='vcan0', bitrate=1000000)
#network.connect(bustype='socketcan', channel='can0', bitrate=1000000)

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

# #convert hex signed 2's complement to int
# def hex2dec(hex_value, datatype): # hex_value = object of rpdo in str matrix, datatype = desired decimal data type
#     if datatype == 'int32': # motor position and velocity data type
#         num_bit = 4
#     if datatype == 'int16': # motor torque data type
#         num_bit = 2
#     # if datatype == 'int32': # crutch force sensor data type
#     #     num_bit = 2
    
#     hex_seg = [0]*num_bit
#     for i in range(num_bit):
#         hex_seg[i] = hex_str[0:2]

#     return 

# #convert int to hex signed 2's complement
# def dec2hex(dec_value, datatype): # hex_value = object of rpdo in str matrix, datatype = desired decimal data type
#     if datatype == 'int32': # motor position and velocity data type
#         num_bit = 4
#     if datatype == 'int16': # motor torque data type
#         num_bit = 2
#     # if datatype == 'int32': # crutch force sensor data type
#     #     num_bit = 2

#     valueInByte = (dec_value).to_bytes(num_bit, byteorder="little", signed=True)
#     # hexadecimal_result = format(dec_value, "03X")
#     # hex_str = hexadecimal_result.zfill(num_bit*2)
#     hex_seg = [0]*num_bit
#     for i in range(num_bit):
#         hex_seg[i] = valueInByte[0+i:1+i]
#     return hex_seg

def process_rpdo(message): # "message" type: 'canopen.pdo.base.Map'; var type: 'canopen.pdo.base.Variable'  
    print('%s received' % message.name)
    cob_id = str(hex(message.cob_id))
    # Add crutch sensor pdo criteria by message.cob_id

    # (message.arbitration_id, message.data) 'Map' object has no attribute 'arbitration_id' ???
    splited_hex = [0]*int((len(message)))
    i = 0
    
    for var in message:
        splited_hex[i] = var.raw
        i = i+1
        # print('%s = %d' % (var.name, var.raw)) # var.name = str; var.raw = int(Raw representation of the object.)
        # print(type(splited_hex[0]))
    if cob_id[2:4] == '28': # if rpdo is 0x2-- , split msg into position and velocity
        # split list > create bytes class > convert bytes to int in little-endian
        position = int.from_bytes(bytes(splited_hex[0:4]), byteorder='little', signed=True) 
        velocity = int.from_bytes(bytes(splited_hex[4:8]), byteorder='little', signed=True)
        position_circular.append(position)
        velocity_circular.append(velocity)
        print("position =", position)
        print("velovity =", velocity)
        print("position circular=", position_circular)
        print("velovity circular=", velocity_circular)   
    elif cob_id[2:4] == '38': # if rpdo is 0x3--, set denominator to 1 to extract all msg as torque
        torque = int.from_bytes(bytes(splited_hex), byteorder='little', signed=True)
        torque_circular.append(torque)
        print("torque =", torque)
        print("torque circular=", torque_circular)
    # Config crutch sensor data convertion
    elif cob_id[2:4] == 'f1':
        for i in range(7):
            Left_unsigned16bit_raw[i] = splited_hex[i+1]
    elif cob_id[2:4] == 'f9':
        for i in range(7):
            Right_unsigned16bit_raw[i] = splited_hex[i+1]
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
        print("Left_crutch_data",Left_crutch_data)
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
        print("Right_crutch_data",Right_crutch_data)
    
Left_unsigned16bit_raw = [0]*12
Right_unsigned16bit_raw = [0]*12
Left_crutch_data = [0]*6
Right_crutch_data = [0]*6
position_circular = CircularBuffer.circularlist(4)
velocity_circular = CircularBuffer.circularlist(4)
torque_circular = CircularBuffer.circularlist(4)
input_data = CircularBuffer.circularlist(4)

for i in range(1,num_rpdo):
    Jetson_66.rpdo[i].add_callback(process_rpdo)
    

while(True):
    
    time.sleep(1)
