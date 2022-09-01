import canopen
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
            for line in lines:
                canCommand = ["cansend"]
                canComponent = line.split()
                if self.busOverride is not None:
                    canCommand.append(self.busOverride)
                else:
                    canCommand.append(canComponent[0]) #bus
                msg = "{}#".format(canComponent[1]) #node id
                for data in canComponent[3:]:
                    msg = msg + data
                canCommand.append(msg)
                os.system(' '.join(canCommand))
                time.sleep(0.001)


if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', help='file with the CAN messages')
    parser.add_argument('--bus', help='which bus to send on', default=None)
    args = parser.parse_args()
    cansim = CANSimulator(args.file, args.bus)
    cansim.Dump()


        
    