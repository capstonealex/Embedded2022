import canopen
import time

# construct a CAN network
network = canopen.Network()

# connect to the CAN network
network.connect(bustype='socketcan', channel='vcan0', bitrate=1000000)

# add node 
Exo_test = canopen.RemoteNode(1, 'Exo_test.eds')
network.add_node(Exo_test)

#set to pre-operational mode
Exo_test.nmt.send_command(0x80)
time.sleep(2)

#config PDO 
print("config PDO device")
Exo_test.rpdo.read()
Exo_test.tpdo.read()
# print("tpdo map (before):\t{}".format(Exo_test.tpdo[1].map))
# print("tpdo enabled (before):\t{}".format(Exo_test.tpdo[1].enabled))
# Manually add the manufacture specific variable, only need if not config in OD
# Exo_test.tpdo[1].add_variable(0x2000, 1, 8) 

# print("tpdo map (after):\t{}".format(Exo_test.tpdo[1].map))
# print("tpdo enabled (after):\t{}".format(Exo_test.tpdo[1].enabled))

#set to operational mode
print("set to operational mode")
Exo_test.nmt.send_command(0x01)
time.sleep(2)


#convert hex signed 2's complement to int
# def hex2dec(hex_value, datatype): # hex_value = object of rpdo in str matrix, datatype = desired decimal data type
#     if datatype == 'int32': # motor position and velocity data type
#         num_byte = 4
#     if datatype == 'int16': # motor torque data type
#         num_byte = 2
#     # if datatype == 'int32': # crutch force sensor data type
#     #     num_byte = 2
    
#     hex_seg = [0]*num_byte
#     for i in range(num_byte):
#         hex_seg[i] = hex_str[0:2]

#     return 

#convert int to hex signed 2's complement
def dec2hex(dec_value, datatype): # hex_value = object of rpdo in str matrix, datatype = desired decimal data type
    if datatype == 'int32': # motor position and velocity data type
        num_byte = 4
    if datatype == 'int16': # motor torque data type
        num_byte = 2
    # if datatype == 'int32': # crutch force sensor data type
    #     num_byte = 2

    valueInByte = (dec_value).to_bytes(num_byte, byteorder="little", signed=True) # signed=True: include negative int
    # hexadecimal_result = format(dec_value, "03X")
    # hex_str = hexadecimal_result.zfill(num_byte*2)
    hex_seg = [0]*num_byte
    for i in range(num_byte):
        hex_seg[i] = int.from_bytes(valueInByte[0+i:1+i], byteorder="little")
    return hex_seg

# def config_pdo(value):
#     input_value = [value]*6
#     for i in range(len(input_value)):
#         input_value[i] = value - 16*i
    
def crutch2can(value, datatype): #convert a float to 2 one bye can message force_H and force_L
    if datatype == 'force': # motor position and velocity data type
        den = 50
    if datatype == 'torque': # motor torque data type
        den = 2000
    signed16bit_raw = int(value*den)
    #convert unsigned 16 bit to signed 16 bit: signed int16 = unsigned int16 - 2^16
    unsigned16bit_raw = signed16bit_raw + 2^16
    # signed=False: NOT include negative int
    # 2: 2 byte means int16
    num_byte = 2
    valueInByte = (unsigned16bit_raw).to_bytes(num_byte, byteorder="big", signed=True) 
    hex_seg = [0]*num_byte
    for i in range(num_byte):
        hex_seg[i] = int.from_bytes(valueInByte[0+i:1+i], byteorder="big")
    return hex_seg

def config_all(value):
    splited_value_1 = 0
    splited_value_2 = 0
    # pdo 1
    splited_value_1 = dec2hex(value, 'int32')
    splited_value_2 = dec2hex(value-16, 'int32')
    # print("splited_value_1 = ",splited_value_1)
    # print("splited_value_2 = ",splited_value_2)
    Exo_test.tpdo[1][0x200F].raw = splited_value_1[0]
    Exo_test.tpdo[1][0x2010].raw = splited_value_1[1]
    Exo_test.tpdo[1][0x2011].raw = splited_value_1[2]
    Exo_test.tpdo[1][0x2012].raw = splited_value_1[3]
    Exo_test.tpdo[1][0x2013].raw = splited_value_2[0]
    Exo_test.tpdo[1][0x2014].raw = splited_value_2[1]
    Exo_test.tpdo[1][0x2015].raw = splited_value_2[2]
    Exo_test.tpdo[1][0x2016].raw = splited_value_2[3]
    # pdo 2
    splited_value_1 = dec2hex(value, 'int16')
    Exo_test.tpdo[2][0x2017].raw = splited_value_1[0]
    Exo_test.tpdo[2][0x2018].raw = splited_value_1[1]
    # pdo 3
    splited_value_1 = dec2hex(value, 'int32')
    splited_value_2 = dec2hex(value-16, 'int32')
    Exo_test.tpdo[3][0x2019].raw = splited_value_1[0]
    Exo_test.tpdo[3][0x201A].raw = splited_value_1[1]
    Exo_test.tpdo[3][0x201B].raw = splited_value_1[2]
    Exo_test.tpdo[3][0x201C].raw = splited_value_1[3]
    Exo_test.tpdo[3][0x201D].raw = splited_value_2[0]
    Exo_test.tpdo[3][0x201E].raw = splited_value_2[1]
    Exo_test.tpdo[3][0x201F].raw = splited_value_2[2]
    Exo_test.tpdo[3][0x2020].raw = splited_value_2[3]
    # pdo 4
    splited_value_1 = dec2hex(value, 'int16')
    Exo_test.tpdo[4][0x2021].raw = splited_value_1[0]
    Exo_test.tpdo[4][0x2022].raw = splited_value_1[1]
    # pdo 5
    splited_value_1 = dec2hex(value, 'int32')
    splited_value_2 = dec2hex(value-16, 'int32')
    Exo_test.tpdo[5][0x2023].raw = splited_value_1[0]
    Exo_test.tpdo[5][0x2024].raw = splited_value_1[1]
    Exo_test.tpdo[5][0x2025].raw = splited_value_1[2]
    Exo_test.tpdo[5][0x2026].raw = splited_value_1[3]
    Exo_test.tpdo[5][0x2027].raw = splited_value_2[0]
    Exo_test.tpdo[5][0x2028].raw = splited_value_2[1]
    Exo_test.tpdo[5][0x2029].raw = splited_value_2[2]
    Exo_test.tpdo[5][0x202A].raw = splited_value_2[3]
    # pdo 6
    splited_value_1 = dec2hex(value, 'int16')
    Exo_test.tpdo[6][0x202B].raw = splited_value_1[0]
    Exo_test.tpdo[6][0x202C].raw = splited_value_1[1]
    # pdo 7
    splited_value_1 = dec2hex(value, 'int32')
    splited_value_2 = dec2hex(value-16, 'int32')
    Exo_test.tpdo[7][0x202D].raw = splited_value_1[0]
    Exo_test.tpdo[7][0x202E].raw = splited_value_1[1]
    Exo_test.tpdo[7][0x202F].raw = splited_value_1[2]
    Exo_test.tpdo[7][0x2030].raw = splited_value_1[3]
    Exo_test.tpdo[7][0x2031].raw = splited_value_2[0]
    Exo_test.tpdo[7][0x2032].raw = splited_value_2[1]
    Exo_test.tpdo[7][0x2033].raw = splited_value_2[2]
    Exo_test.tpdo[7][0x2034].raw = splited_value_2[3]
    # pdo 8
    splited_value_1 = dec2hex(value, 'int16')
    Exo_test.tpdo[8][0x2035].raw = splited_value_1[0]
    Exo_test.tpdo[8][0x2036].raw = splited_value_1[1]
    # pdo 9 & 10
    #convert unsigned 16 bit to signed 16 bit: signed int16 = unsigned int16 - 2^16
    crutch_input_force_data = value/50
    crutch_input_torque_data = value/2000
    force_can = crutch2can(crutch_input_force_data, "force")
    torque_can = crutch2can(crutch_input_torque_data, "torque")
    Exo_test.tpdo[9][0x2037].raw = 0
    Exo_test.tpdo[9][0x2038].raw = force_can[0]
    Exo_test.tpdo[9][0x2039].raw = force_can[1]
    Exo_test.tpdo[9][0x203A].raw = force_can[0]
    Exo_test.tpdo[9][0x203B].raw = force_can[1]
    Exo_test.tpdo[9][0x203C].raw = force_can[0]
    Exo_test.tpdo[9][0x203D].raw = force_can[1]
    Exo_test.tpdo[9][0x203E].raw = torque_can[0]
    Exo_test.tpdo[10][0x203F].raw = torque_can[1]
    Exo_test.tpdo[10][0x2040].raw = torque_can[0]
    Exo_test.tpdo[10][0x2041].raw = torque_can[1]
    Exo_test.tpdo[10][0x2042].raw = torque_can[0]
    Exo_test.tpdo[10][0x2043].raw = torque_can[1]
    Exo_test.tpdo[10][0x2044].raw = 0
    Exo_test.tpdo[10][0x2045].raw = 0
    Exo_test.tpdo[10][0x2046].raw = 0
    # pdo 11 & 12
    #convert unsigned 16 bit to signed 16 bit: signed int16 = unsigned int16 - 2^16
    crutch_input_force_data = value/50
    crutch_input_torque_data = value/2000
    force_can = crutch2can(crutch_input_force_data, "force")
    torque_can = crutch2can(crutch_input_torque_data, "torque")
    Exo_test.tpdo[11][0x2047].raw = 0
    Exo_test.tpdo[11][0x2048].raw = force_can[0]
    Exo_test.tpdo[11][0x2049].raw = force_can[1]
    Exo_test.tpdo[11][0x204A].raw = force_can[0]
    Exo_test.tpdo[11][0x204B].raw = force_can[1]
    Exo_test.tpdo[11][0x204C].raw = force_can[0]
    Exo_test.tpdo[11][0x204D].raw = force_can[1]
    Exo_test.tpdo[11][0x204E].raw = torque_can[0]
    Exo_test.tpdo[12][0x204F].raw = torque_can[1]
    Exo_test.tpdo[12][0x2050].raw = torque_can[0]
    Exo_test.tpdo[12][0x2051].raw = torque_can[1]
    Exo_test.tpdo[12][0x2052].raw = torque_can[0]
    Exo_test.tpdo[12][0x2053].raw = torque_can[1]
    Exo_test.tpdo[12][0x2054].raw = 0
    Exo_test.tpdo[12][0x2055].raw = 0
    Exo_test.tpdo[12][0x2056].raw = 0

# test sending PDO to set output
print("test sending PDO to set output")

test_id = 0
# test list: (ignore this list)
# id = 0: No one
# id = 1: All
# id = 2: Left Hip Motor
# id = 3: Left Knee Motor
# id = 4: Right Hip Motor
# id = 5: Right Knee Motor
# id = 6: Left Crutch
# id = 7: Right Crutch
# id = 8: Logger
# id = 9: Main Exo Controller
# id = 10: Crutch UI Controller


def transmit_pdo(id, value):
    splited_value_1 = 0
    splited_value_2 = 0
    print("Testing TPDO:",id )
    config_all(value)
    if(id==0): # transmit ALL PDO
        for i in range(1,13):
            Exo_test.tpdo[i].transmit()
    elif(id==1):
        print("TPDO Transmit value = ", write_data, write_data-16)
        Exo_test.tpdo[id].transmit()
    elif(id==2):
        print("TPDO Transmit value = ", write_data)
        Exo_test.tpdo[id].transmit()
    elif(id==3):
        print("TPDO Transmit value = ", write_data, write_data-16)
        Exo_test.tpdo[id].transmit()
    elif(id==4):
        print("TPDO Transmit value = ", write_data)
        Exo_test.tpdo[id].transmit()
    elif(id==5):
        print("TPDO Transmit value = ", write_data, write_data-16)
        Exo_test.tpdo[id].transmit()
    elif(id==6):
        print("TPDO Transmit value = ", write_data)
        Exo_test.tpdo[id].transmit()
    elif(id==7):
        print("TPDO Transmit value = ", write_data, write_data-16)
        Exo_test.tpdo[id].transmit()
    elif(id==8):
        print("TPDO Transmit value = ", write_data)
        Exo_test.tpdo[id].transmit()
    elif(id==9):
        print("TPDO Transmit value = ", write_data/50, write_data/2000)
        Exo_test.tpdo[id].transmit()
        Exo_test.tpdo[id+1].transmit()
    elif(id==10):
        print("Testing TPDO:",id)
    elif(id==11):
        print("TPDO Transmit value = ", write_data/50, write_data/2000)
        Exo_test.tpdo[id].transmit()
        Exo_test.tpdo[id+1].transmit()
    elif(id==12):
        print("Testing TPDO:",id)
    elif(id==13):
        print("Testing TPDO:",id)
    elif(id==14):
        print("Testing TPDO:",id)
    elif(id==15):
        print("Testing TPDO:",id)
    elif(id==16):
        print("Testing TPDO:",id)
    elif(id==17):
        print("Testing TPDO:",id)
    elif(id==18):
        print("Testing TPDO:",id)
    
    
    

    
    

try:
    write_data = -20
    
    while True:
        write_data += 1

        position_data = dec2hex(write_data, 'int32')

        transmit_pdo(test_id, write_data)
        # if write_data > 0xFF:
        #     write_data = 0
        # print("position_data: %d",position_data)
        # print(type(position_data[0]))
        # Exo_test.tpdo[1][0x200F].raw = position_data[0]
        # Exo_test.tpdo[1][0x2010].raw = position_data[1]
        # Exo_test.tpdo[1][0x2011].raw = position_data[2]
        # Exo_test.tpdo[1][0x2012].raw = position_data[3]
        # Exo_test.tpdo[1][0x2004].raw = write_data
        # Exo_test.tpdo[1][0x2005].raw = write_data
        # Exo_test.tpdo[1][0x2006].raw = write_data
        # Exo_test.tpdo[1][0x2007].raw = write_data
        # print("TPDO Transmit value = ", write_data)
        # print("before value = {}".format(Exo_test.tpdo[1][0x2004].raw))
        # print("before value = {}".format(Exo_test.tpdo[1][0x2005].raw))
        # print("before value = {}".format(Exo_test.tpdo[1][0x2006].raw))
        # print("before value = {}".format(Exo_test.tpdo[1][0x2007].raw))

        # Exo_test.tpdo[1].transmit()
        # print("write output value = {}".format(Exo_test.tpdo[1][0x2000].raw))
        time.sleep(0.1)
except KeyboardInterrupt:
    print("exit from sending PDO to Jetson")

# loop
while 1:
    time.sleep(1)
    print("slaver work")
    #slaver_node_2.tpdo[1].transmit()