sudo ip link set can0 down
sudo ip link set can1 down
sudo ip link set can0 up type can bitrate 1000000 loopback on
sudo ip link set can1 up type can bitrate 1000000
sudo ifconfig can0 txqueuelen 65536
sudo ifconfig can1 txqueuelen 65536
