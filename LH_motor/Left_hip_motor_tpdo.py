import canopen
import time

# construct a CAN network
network = canopen.Network()

# connect to the CAN network
network.connect(bustype='socketcan', channel='vcan0', bitrate=1000000)

# add node 
Left_hip_motor_node_1 = canopen.RemoteNode(1, 'Left_hip_motor_node_1.eds')
network.add_node(Left_hip_motor_node_1)

#set to pre-operational mode
Left_hip_motor_node_1.nmt.send_command(0x80)
time.sleep(2)

#config PDO 
print("config PDO device")
Left_hip_motor_node_1.rpdo.read()
Left_hip_motor_node_1.tpdo.read()
print("tpdo map (before):\t{}".format(Left_hip_motor_node_1.tpdo[1].map))
print("tpdo enabled (before):\t{}".format(Left_hip_motor_node_1.tpdo[1].enabled))
# Manually add the manufacture specific variable, only need if not config in OD
# Left_hip_motor_node_1.tpdo[1].add_variable(0x2000, 1, 8) 

print("tpdo map (after):\t{}".format(Left_hip_motor_node_1.tpdo[1].map))
print("tpdo enabled (after):\t{}".format(Left_hip_motor_node_1.tpdo[1].enabled))

#set to operational mode
print("set to operational mode")
Left_hip_motor_node_1.nmt.send_command(0x01)
time.sleep(2)


#convert hex signed 2's complement to int
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

#convert int to hex signed 2's complement
def dec2hex(dec_value, datatype): # hex_value = object of rpdo in str matrix, datatype = desired decimal data type
    if datatype == 'int32': # motor position and velocity data type
        num_bit = 4
    if datatype == 'int16': # motor torque data type
        num_bit = 2
    # if datatype == 'int32': # crutch force sensor data type
    #     num_bit = 2

    valueInByte = (dec_value).to_bytes(num_bit, byteorder="little", signed=True) # signed=True: include negative int
    # hexadecimal_result = format(dec_value, "03X")
    # hex_str = hexadecimal_result.zfill(num_bit*2)
    hex_seg = [0]*num_bit
    for i in range(num_bit):
        hex_seg[i] = int.from_bytes(valueInByte[0+i:1+i], byteorder="little")
    return hex_seg

# test sending PDO to set output
print("test sending PDO to set output")
try:
    write_data = -20
    
    while True:
        write_data += 1

        position_data = dec2hex(write_data, 'int32')
        # if write_data > 0xFF:
        #     write_data = 0
        # print("position_data: %d",position_data)
        # print(type(position_data[0]))
        Left_hip_motor_node_1.tpdo[1][0x2000].raw = position_data[0]
        Left_hip_motor_node_1.tpdo[1][0x2001].raw = position_data[1]
        Left_hip_motor_node_1.tpdo[1][0x2002].raw = position_data[2]
        Left_hip_motor_node_1.tpdo[1][0x2003].raw = position_data[3]
        # Left_hip_motor_node_1.tpdo[1][0x2004].raw = write_data
        # Left_hip_motor_node_1.tpdo[1][0x2005].raw = write_data
        # Left_hip_motor_node_1.tpdo[1][0x2006].raw = write_data
        # Left_hip_motor_node_1.tpdo[1][0x2007].raw = write_data
        print("TPDO Transmit value = ", write_data)
        # print("before value = {}".format(Left_hip_motor_node_1.tpdo[1][0x2004].raw))
        # print("before value = {}".format(Left_hip_motor_node_1.tpdo[1][0x2005].raw))
        # print("before value = {}".format(Left_hip_motor_node_1.tpdo[1][0x2006].raw))
        # print("before value = {}".format(Left_hip_motor_node_1.tpdo[1][0x2007].raw))

        Left_hip_motor_node_1.tpdo[1].transmit()
        # print("write output value = {}".format(Left_hip_motor_node_1.tpdo[1][0x2000].raw))
        time.sleep(0.1)
except KeyboardInterrupt:
    print("exit from sending PDO to Jetson")

# loop
while 1:
    time.sleep(1)
    print("slaver work")
    #slaver_node_2.tpdo[1].transmit()