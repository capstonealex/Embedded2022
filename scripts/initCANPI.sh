modprobe vcan
sudo ip link set vcan0 down
sudo ip link set vcan0 up
sudo ifconfig vcan0 txqueuelen 65536
