import time
import os
import argparse
import time
class CANSimulator:

    def __init__(self, fileName, busOverride = None):
        self.fileName = fileName
        self.busOverride = busOverride

    def Dump(self):
      
        with open(self.fileName, 'r') as fp:
            lines = fp.readlines()
            if self.busOverride is not None:
                bus = self.busOverride
            else:
                bus = lines[0].split()[0] 
            for line in lines:
                canComponent = line.split()
                canCommand = "cansend {0} {1}#{2}".format(bus, canComponent[1],''.join(canComponent[3:]))
                os.system(canCommand)
                #time.sleep(0.002) # this delay has to be above 0.002s 


if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', help='file with the CAN messages')
    parser.add_argument('--bus', help='which bus to send on', default=None)
    args = parser.parse_args()
    cansim = CANSimulator(args.file, args.bus)
    cansim.Dump()


        
    