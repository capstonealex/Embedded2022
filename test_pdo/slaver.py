import canopen
import time

# construct a CAN network
network = canopen.Network()

# connect to the CAN network
network.connect(bustype='socketcan', channel='vcan0', bitrate=1000000)
#network.connect(bustype='socketcan', channel='can0', bitrate=1000000)

# create a slaver node with id 2(need to match with master.py) and Object Dictionary "Slaver.eds"
slaver_node_2 = network.create_node(2, 'LC5100.eds')



# Node send the boot-up message to the CAN network COB-ID:0x700+node-ID detail: "0"
slaver_node_2.nmt.send_command(0)

# With the heartbeat configuration in object Dictionary, use the function by following command every 1s(1000ms)
slaver_node_2.nmt.start_heartbeat(1000)  

# send pdo message
slaver_node_2.rpdo.read()
slaver_node_2.tpdo.read()
#slaver_node_2.rpdo[1].transmit()

#slaver_node_2.tpdo[1]['Application Commands.Command Speed'].phys = 100
#slaver_node_2.tpdo[1].start(0.1)
print("Test reading PDO to read input of Remote I/O LC5100")
try:
    while True:
        timestamp = slaver_node_2.tpdo[1].wait_for_reception()
        read_value = slaver_node_2.tpdo[1][0x2000].raw
        print("Read input value = {}, t={}".format(read_value, timestamp))
    
except KeyboardInterrupt:
    print("Exit from reading PDO to LC5100")
# loop
#while 1:
#    time.sleep(1)
#    print("slaver work")
    #slaver_node_2.tpdo[1].transmit()