## @package NetworkClass
# Interface for network objects
# CAN and ethernet in the future 
from abc import abstractmethod
class Network():
    @abstractmethod
    def Setup(self):
    ## Setup the connection object
        pass

    def Update(self): 
    ## Any frequency dependent update of states goes here
        pass

    def SetupHardware(self):
    ## For setting up hardware (might not be in use
        pass



