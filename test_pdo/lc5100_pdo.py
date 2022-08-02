import canopen
import time

# construct a CAN network
network = canopen.Network()

# connect to the CAN network
network.connect(bustype='socketcan', channel='vcan0', bitrate=1000000)

# add node 
Jetson_node_2 = canopen.RemoteNode(2, 'LC5100.eds')
#slaver_node_2 = canopen.RemoteNode(2, 'node2.eds')
network.add_node(Jetson_node_2)

#set to pre-operational mode
Jetson_node_2.nmt.send_command(0x80)
time.sleep(5)

#config PDO 
print("config PDO device")
Jetson_node_2.rpdo.read()
Jetson_node_2.tpdo.read()
print("tpdo map (before):\t{}".format(Jetson_node_2.tpdo[1].map))
print("tpdo enabled (before):\t{}".format(Jetson_node_2.tpdo[1].enabled))
Jetson_node_2.tpdo[1].add_variable(0x2000, 1, 8)
print("tpdo map (after):\t{}".format(Jetson_node_2.tpdo[1].map))
print("tpdo enabled (after):\t{}".format(Jetson_node_2.tpdo[1].enabled))

#set to operational mode
print("set to operational mode")
Jetson_node_2.nmt.send_command(0x01)
time.sleep(3)

# test sending PDO to set output
print("test sending PDO to set output")
try:
    write_data = 0
    while True:
        write_data += 1
        if write_data > 0xFF:
            write_data = 0
        print("write output value = {}".format(write_data))
        Jetson_node_2.tpdo[1][0x2000].raw = write_data
        Jetson_node_2.tpdo[1].transmit()
        time.sleep(1)
except KeyboardInterrupt:
    print("exit from sending PDO to Jetson")

# loop
while 1:
    time.sleep(1)
    print("slaver work")
    #slaver_node_2.tpdo[1].transmit()