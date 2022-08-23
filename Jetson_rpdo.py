import canopen
import time

# construct a CAN network
network = canopen.Network()

# connect to the CAN network
network.connect(bustype='socketcan', channel='vcan0', bitrate=1000000)
#network.connect(bustype='socketcan', channel='can0', bitrate=1000000)

# create a slaver node with id 2(need to match with master.py) and Object Dictionary "Slaver.eds"
Jetson_66 = network.create_node(66, 'Jetson_66_v11.eds')

# Node send the boot-up message to the CAN network COB-ID:0x700+node-ID detail: "0"
Jetson_66.nmt.send_command(0)

# With the heartbeat configuration in object Dictionary, use the function by following command every 1s(1000ms)
Jetson_66.nmt.start_heartbeat(1000)  

# send pdo message
Jetson_66.rpdo.read()
Jetson_66.tpdo.read()

print("Test reading PDO to read input of Exo")

def print_pdo(message):
    print('%s received' % message.name)
    for var in message:
        print('%s = %d' % (var.name, var.raw))


Jetson_66.rpdo[1].add_callback(print_pdo)
Jetson_66.rpdo[2].add_callback(print_pdo)
Jetson_66.rpdo[3].add_callback(print_pdo)
Jetson_66.rpdo[4].add_callback(print_pdo)
Jetson_66.rpdo[5].add_callback(print_pdo)
Jetson_66.rpdo[6].add_callback(print_pdo)
Jetson_66.rpdo[7].add_callback(print_pdo)
Jetson_66.rpdo[8].add_callback(print_pdo)
Jetson_66.rpdo[9].add_callback(print_pdo)
Jetson_66.rpdo[10].add_callback(print_pdo)
Jetson_66.rpdo[11].add_callback(print_pdo)
Jetson_66.rpdo[12].add_callback(print_pdo)
Jetson_66.rpdo[13].add_callback(print_pdo)
Jetson_66.rpdo[14].add_callback(print_pdo)
Jetson_66.rpdo[15].add_callback(print_pdo)
Jetson_66.rpdo[16].add_callback(print_pdo)
Jetson_66.rpdo[17].add_callback(print_pdo)
Jetson_66.rpdo[18].add_callback(print_pdo)


while(True):
    time.sleep(1)
