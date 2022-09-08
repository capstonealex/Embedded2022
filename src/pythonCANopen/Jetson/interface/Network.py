## @package INetworkClass
# Interface for network objects
# Ethernet and CAN 
from abc import abstractmethod
class Network():
    @abstractmethod
    def Setup(self):
    ## Setup the connection object
        pass

    def Update(self): 
    ## Polling goes here 
        pass

    def SetupHardware(self):
    ## For setting up hardware (might not be in use
        pass



