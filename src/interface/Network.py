## @package NetworkClass
# Interface for network objects
# Ethernet and CAN 
from abc import abstractmethod

class Network():
    @abstractmethod
    def Setup(self):
    ## Setup the connection object
        pass
    @abstractmethod
    def Update(self): 
    ## Polling goes here 
        pass
    @abstractmethod
    def SetupHardware(self):
    ## For setting up hardware (not in use)
        pass



