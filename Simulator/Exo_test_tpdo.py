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


test_id = 9


def config_pdo(id, value):
    splited_value_1 = 0
    splited_value_2 = 0
    print("Testing TPDO:",id )
    if(id==1):
        splited_value_1 = dec2hex(write_data, 'int32')
        splited_value_2 = dec2hex(write_data-16, 'int32')
        Exo_test.tpdo[id][0x200F].raw = splited_value_1[0]
        Exo_test.tpdo[id][0x2010].raw = splited_value_1[1]
        Exo_test.tpdo[id][0x2011].raw = splited_value_1[2]
        Exo_test.tpdo[id][0x2012].raw = splited_value_1[3]
        Exo_test.tpdo[id][0x2013].raw = splited_value_2[0]
        Exo_test.tpdo[id][0x2014].raw = splited_value_2[1]
        Exo_test.tpdo[id][0x2015].raw = splited_value_2[2]
        Exo_test.tpdo[id][0x2016].raw = splited_value_2[3]
        print("TPDO Transmit value = ", write_data, write_data-16)
    elif(id==2):
        splited_value_1 = dec2hex(write_data, 'int16')
        Exo_test.tpdo[id][0x2017].raw = splited_value_1[0]
        Exo_test.tpdo[id][0x2018].raw = splited_value_1[1]
        print("TPDO Transmit value = ", write_data)
    elif(id==3):
        splited_value_1 = dec2hex(write_data, 'int32')
        splited_value_2 = dec2hex(write_data-16, 'int32')
        Exo_test.tpdo[id][0x2019].raw = splited_value_1[0]
        Exo_test.tpdo[id][0x201A].raw = splited_value_1[1]
        Exo_test.tpdo[id][0x201B].raw = splited_value_1[2]
        Exo_test.tpdo[id][0x201C].raw = splited_value_1[3]
        Exo_test.tpdo[id][0x201D].raw = splited_value_2[0]
        Exo_test.tpdo[id][0x201E].raw = splited_value_2[1]
        Exo_test.tpdo[id][0x201F].raw = splited_value_2[2]
        Exo_test.tpdo[id][0x2020].raw = splited_value_2[3]
        print("TPDO Transmit value = ", write_data, write_data-16)
    elif(id==4):
        splited_value_1 = dec2hex(write_data, 'int16')
        Exo_test.tpdo[id][0x2021].raw = splited_value_1[0]
        Exo_test.tpdo[id][0x2022].raw = splited_value_1[1]
        print("TPDO Transmit value = ", write_data)
    elif(id==5):
        splited_value_1 = dec2hex(write_data, 'int32')
        splited_value_2 = dec2hex(write_data-16, 'int32')
        Exo_test.tpdo[id][0x2023].raw = splited_value_1[0]
        Exo_test.tpdo[id][0x2024].raw = splited_value_1[1]
        Exo_test.tpdo[id][0x2025].raw = splited_value_1[2]
        Exo_test.tpdo[id][0x2026].raw = splited_value_1[3]
        Exo_test.tpdo[id][0x2027].raw = splited_value_2[0]
        Exo_test.tpdo[id][0x2028].raw = splited_value_2[1]
        Exo_test.tpdo[id][0x2029].raw = splited_value_2[2]
        Exo_test.tpdo[id][0x202A].raw = splited_value_2[3]
        print("TPDO Transmit value = ", write_data, write_data-16)
    elif(id==6):
        splited_value_1 = dec2hex(write_data, 'int16')
        Exo_test.tpdo[id][0x202B].raw = splited_value_1[0]
        Exo_test.tpdo[id][0x202C].raw = splited_value_1[1]
        print("TPDO Transmit value = ", write_data)
    elif(id==7):
        splited_value_1 = dec2hex(write_data, 'int32')
        splited_value_2 = dec2hex(write_data-16, 'int32')
        Exo_test.tpdo[id][0x202D].raw = splited_value_1[0]
        Exo_test.tpdo[id][0x202E].raw = splited_value_1[1]
        Exo_test.tpdo[id][0x202F].raw = splited_value_1[2]
        Exo_test.tpdo[id][0x2030].raw = splited_value_1[3]
        Exo_test.tpdo[id][0x2031].raw = splited_value_2[0]
        Exo_test.tpdo[id][0x2032].raw = splited_value_2[1]
        Exo_test.tpdo[id][0x2033].raw = splited_value_2[2]
        Exo_test.tpdo[id][0x2034].raw = splited_value_2[3]
        print("TPDO Transmit value = ", write_data, write_data-16)
    elif(id==8):
        splited_value_1 = dec2hex(write_data, 'int16')
        Exo_test.tpdo[id][0x2035].raw = splited_value_1[0]
        Exo_test.tpdo[id][0x2036].raw = splited_value_1[1]
        print("TPDO Transmit value = ", write_data)
    elif(id==9):
        print("Testing TPDO:",id)
        splited_value_1 = dec2hex(write_data, 'int32')
        splited_value_2 = dec2hex(write_data-16, 'int32')
        Exo_test.tpdo[id][0x2037].raw = splited_value_1[0]
        Exo_test.tpdo[id][0x2038].raw = splited_value_1[1]
        Exo_test.tpdo[id][0x2039].raw = splited_value_1[2]
        Exo_test.tpdo[id][0x203A].raw = splited_value_1[3]
        Exo_test.tpdo[id][0x203B].raw = splited_value_2[0]
        Exo_test.tpdo[id][0x203C].raw = splited_value_2[1]
        Exo_test.tpdo[id][0x203D].raw = splited_value_2[2]
        Exo_test.tpdo[id][0x203E].raw = splited_value_2[3]
        print("TPDO Transmit value = ", write_data, write_data-16)
    elif(id==10):
        print("Testing TPDO:",id)
    elif(id==11):
        print("Testing TPDO:",id)
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
    
    Exo_test.tpdo[id].transmit()
    
    

    
    

try:
    write_data = -20
    
    while True:
        write_data += 1

        position_data = dec2hex(write_data, 'int32')

        config_pdo(test_id, write_data)
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