import CANNetwork






if __name__ == "__main__":
    network = CANNetwork()
    network.Setup()

    while True:
        network.Update()