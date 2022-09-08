sudo ip link set can0 down
sudo ip link set can0 up type can bitrate 1000000 loopback on
sudo ifconfig can0 txqueuelen 65536
