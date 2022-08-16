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

# test sending PDO to set output
print("test sending PDO to set output")
try:
    write_data = 0
    while True:
        write_data += 1
        if write_data > 0xFF:
            write_data = 0
        
        Left_hip_motor_node_1.tpdo[1][0x2000].raw = write_data
        Left_hip_motor_node_1.tpdo[1][0x2001].raw = write_data
        Left_hip_motor_node_1.tpdo[1][0x2002].raw = write_data
        Left_hip_motor_node_1.tpdo[1][0x2003].raw = write_data
        Left_hip_motor_node_1.tpdo[1][0x2004].raw = write_data
        Left_hip_motor_node_1.tpdo[1][0x2005].raw = write_data
        Left_hip_motor_node_1.tpdo[1][0x2006].raw = write_data
        Left_hip_motor_node_1.tpdo[1][0x2007].raw = write_data
        print("before value = {}".format(Left_hip_motor_node_1.tpdo[1][0x2000].raw))
        print("before value = {}".format(Left_hip_motor_node_1.tpdo[1][0x2001].raw))
        print("before value = {}".format(Left_hip_motor_node_1.tpdo[1][0x2002].raw))
        print("before value = {}".format(Left_hip_motor_node_1.tpdo[1][0x2003].raw))
        print("before value = {}".format(Left_hip_motor_node_1.tpdo[1][0x2004].raw))
        print("before value = {}".format(Left_hip_motor_node_1.tpdo[1][0x2005].raw))
        print("before value = {}".format(Left_hip_motor_node_1.tpdo[1][0x2006].raw))
        print("before value = {}".format(Left_hip_motor_node_1.tpdo[1][0x2007].raw))

        Left_hip_motor_node_1.tpdo[1].transmit()
        print("write output value = {}".format(Left_hip_motor_node_1.tpdo[1][0x2000].raw))
        time.sleep(1)
except KeyboardInterrupt:
    print("exit from sending PDO to Jetson")

# loop
while 1:
    time.sleep(1)
    print("slaver work")
    #slaver_node_2.tpdo[1].transmit()