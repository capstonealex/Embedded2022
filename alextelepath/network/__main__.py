from .CANNetwork import CANNetwork

try:
    can = CANNetwork(66, 20, 'Jetson_66_v21.eds', [], True)
    print("success in creating can")

except Exception: 
    print("something went wrong")