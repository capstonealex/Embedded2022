from sys import byteorder
import canopen
# import cantools
import time
import CircularBuffer

num_rpdo = 18 #1-8: exo motor; 9-12: crutch sensor

# construct a CAN network
network = canopen.Network()

# connect to the CAN network
# network.connect(bustype='socketcan', channel='vcan0', bitrate=1000000)
network.connect(bustype='socketcan', channel='can0', bitrate=1000000)

# create a slaver node with id 2(need to match with master.py) and Object Dictionary "Slaver.eds"
Jetson_66 = network.create_node(66, 'Jetson_66_v11.eds')

# Node send the boot-up message to the CAN network COB-ID:0x700+node-ID detail: "0"
Jetson_66.nmt.send_command(0)

# With the heartbeat configuration in object Dictionary, use the function by following command every 1s(1000ms)
Jetson_66.nmt.start_heartbeat(1000)  

# send pdo message
Jetson_66.rpdo.read()
Jetson_66.tpdo.read()

print("CAN BUS configuration completed, waiting RPDO...")

#convert hex signed 2's complement to int
def hex2dec(hex_value, datatype): # hex_value = object of rpdo in str matrix, datatype = desired decimal data type
    if datatype == 'int32': # motor position and velocity data type
        num_bit = 4
    if datatype == 'int16': # motor torque data type
        num_bit = 2
    # if datatype == 'int32': # crutch force sensor data type
    #     num_bit = 2
    
    hex_seg = [0]*num_bit
    for i in range(num_bit):
        hex_seg[i] = hex_str[0:2]

    return 

#convert int to hex signed 2's complement
def dec2hex(dec_value, datatype): # hex_value = object of rpdo in str matrix, datatype = desired decimal data type
    if datatype == 'int32': # motor position and velocity data type
        num_bit = 4
    if datatype == 'int16': # motor torque data type
        num_bit = 2
    # if datatype == 'int32': # crutch force sensor data type
    #     num_bit = 2

    valueInByte = (dec_value).to_bytes(num_bit, byteorder="little", signed=True)
    # hexadecimal_result = format(dec_value, "03X")
    # hex_str = hexadecimal_result.zfill(num_bit*2)
    hex_seg = [0]*num_bit
    for i in range(num_bit):
        hex_seg[i] = valueInByte[0+i:1+i]
    return hex_seg

def process_rpdo(message): # "message" type: 'canopen.pdo.base.Map'; var type: 'canopen.pdo.base.Variable'  
    # print('received message name:',message.name)
    # print('COB-ID:',message.cob_id) not like 0x281 format
    cob_id = str(hex(message.cob_id))
    # Add crutch sensor pdo criteria by message.cob_id

    # (message.arbitration_id, message.data) 'Map' object has no attribute 'arbitration_id' ???
    splited_hex = [0]*int((len(message)))
    i = 0
    for var in message:
        splited_hex[i] = var.raw
        i = i+1
        # print("Got crutch sensor data:", var.raw)
        # print('%s = %d' % (var.name, var.raw)) # var.name = str; var.raw = int(Raw representation of the object.)
        # print(type(splited_hex[0]))
    # if cob_id[2:3] == '2': # if rpdo is 0x2-- , split msg into position and velocity
    #     # split list > create bytes class > convert bytes to int in little-endian
    #     position = int.from_bytes(bytes(splited_hex[0:4]), byteorder='little', signed=True) 
    #     velocity = int.from_bytes(bytes(splited_hex[4:8]), byteorder='little', signed=True)
    #     # position_circular.append(position) #need to fix different id's position into same position circular buffer
    #     # velocity_circular.append(velocity)
    #     print("COB-ID: ",cob_id,", position =", position)
    #     print("COB-ID: ",cob_id,", velocity =", velocity)
    # if cob_id[2:3] == '3': # if rpdo is 0x3--, set denominator to 1 to extract all msg as torque
    #     # torque = int.from_bytes(bytes(splited_hex), byteorder='little')
        # torque_circular.append(torque)
        # print("COB-ID: ",cob_id,", torque =", torque)
        
    
    if cob_id[3] == 'F': # if rpdo is 0xF--, convert to crutch sensor data
          print("Got crutch sensor data:", var.raw)
    
    
    
    
    # print("position circular=", position_circular)
    
    # position_dec = hex2dec(position_hex, byteorder="little")

position_circular = CircularBuffer.circularlist(4)
velocity_circular = CircularBuffer.circularlist(4)
torque_circular = CircularBuffer.circularlist(4)
input_data = CircularBuffer.circularlist(4)

for i in range(1,num_rpdo):
    #   Jetson_66.rpdo[i].add_callback(process_rpdo)
    print(str(hex(Jetson_66.rpdo[i].cob_id)))
    print(Jetson_66.rpdo[i].name)
    
#print(str(hex(Jetson_66.rpdo[0].cob_id)))


while(True):
    
    time.sleep(1)
# CAN BUS configuration completed, waiting RPDO...
# 0x281
# TxPDO2_node1
# 0x282
# TxPDO2_node2
# 0x382
# TxPDO3_node2
# 0x283
# TxPDO2_node3
# 0x383
# TxPDO3_node3
# 0x284
# TxPDO2_node4
# 0x384
# TxPDO3_node4
# 0x0
# Unknown
# 0x0
# Unknown
# 0x0
# Unknown
# 0x0
# Unknown
# 0x0
# Unknown
# 0x0
# Unknown
# 0x0
# Unknown
# 0x0
# Unknown
# 0x0
# Unknown
# 0x0
# Unknown
