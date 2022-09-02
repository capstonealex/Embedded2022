import canopen
import time

# enable the simulated Left hip motor:
# sudo modprobe vcan
# sudo ip link add dev vcan0 type vcan
# sudo ip link set up vcan0
# candump -t d vcan0 #absoluted time:(-t a); related time:(-t d) 

# construct a CAN network
network = canopen.Network()

# connect to the CAN network
network.connect(bustype='socketcan', channel='vcan0', bitrate=1000000)
#network.connect(bustype='socketcan', channel='can0', bitrate=1000000)

# create a slaver node with id 2(need to match with master.py) and Object Dictionary "Slaver.eds"
Left_hip_motor_node_1 = network.create_node(1, 'Left_hip_motor_node_1.eds')

# Node send the boot-up message to the CAN network COB-ID:0x700+node-ID detail: "0"
Left_hip_motor_node_1.nmt.send_command(0)

# With the heartbeat configuration in object Dictionary, use the function by following command every 1s(1000ms)
Left_hip_motor_node_1.nmt.start_heartbeat(1000)  

print("Test reading PDO to read input of Remote I/O LC5100")
try:
    while True:
        Left_hip_motor_node_1.rpdo.read()
        Left_hip_motor_node_1.tpdo.read()

except KeyboardInterrupt:
    print("Exit from reading PDO to LC5100")


