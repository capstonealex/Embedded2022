from CANNetwork import CANNetwork


if __name__ == "__main__":
    network = CANNetwork(66, "Jetson_exo_66.eds")
    network.Setup()
	
    while network.Update():
        pass
