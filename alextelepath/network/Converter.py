class Converter():
## Helper class that converts raw bytes to the actual raw data. 

    def __init__(self):
        self.cobid = None
        self.rawmsg = None
        self.Left_crutch_data = [0]*12
        self.Right_crutch_data = [0]*12
        self.Left_crutch_offset = [25.1,7.2,22.2,0,0,0]
        self.Right_crutch_offset = [-33,32,-11.34,0.074,0.19,3.44]
    
    
    def position(self, rawmsg):
        position = int.from_bytes(bytes(rawmsg[0:4]), byteorder='little', signed=True) 
        #print(position)
        return position

    def velocity(self, rawmsg):
        velocity = int.from_bytes(bytes(rawmsg[4:8]), byteorder='little', signed=True)
       # print(velocity)
        return velocity
    
    def torque(self, rawmsg):
        torque = int.from_bytes(bytes(rawmsg), byteorder='little', signed=True)
        #print(torque)
        return torque
    
    def Left_crutch_data_1(self, rawmsg):
        # for i in range(7):
        #     self.Left_crutch_data[i] = rawmsg[i+1]
        self.Left_crutch_data[0:7] = [rawmsg[i+1] for i in range(7)]
        self.Left_crutch_data[7:12] = [0]*5
        #print(self.Left_crutch_data)
        return self.Left_crutch_data

    def Right_crutch_data_1(self, rawmsg):
        # for i in range(7):
        #    self.Right_crutch_data[i] = rawmsg[i+1]
        self.Right_crutch_data[0:7] = [rawmsg[i+1] for i in range(7)]
        self.Right_crutch_data[7:12] = [0]*5
        #print(self.Right_crutch_data)
        return self.Right_crutch_data

    def Left_crutch_data_2(self, data_1, rawmsg):
        # # for i in range(5):
        # #     data_1[i+7] = rawmsg[i]
        # data_1[7:12] = rawmsg[0:5]
        # for i in range(0,6):
        #     self.Left_crutch_data[i] = int.from_bytes(bytes(data_1[0+2*i:2+2*i]), byteorder='big', signed=True)
        #     #self.Left_crutch_data[i] = self.Left_crutch_data[i] - 2^16
        #     if(i<3):
        #         self.Left_crutch_data[i] = self.Left_crutch_data[i]/50
        #     elif(i>=3):
        #         self.Left_crutch_data[i] = self.Left_crutch_data[i]/2000
        # print(self.Left_crutch_data)
        # return self.Left_crutch_data
         # for i in range(5):
        #     data_1[i+7] = rawmsg[i]
        data_1[7:12] = rawmsg[0:5]
        crutchOut = [0] * 6
        for i in range(0,6):
            crutchOut[i] = int.from_bytes(bytes(data_1[0+2*i:2+2*i]), byteorder='big', signed=True)
            #self.Right_crutch_data[i] = self.Right_crutch_data[i] - 2^16
            if(i<3):
                crutchOut[i] = crutchOut[i]/50
            elif(i>=3):
                crutchOut[i] = crutchOut[i]/2000
        # print("left")
        # print(crutchOut)
        return crutchOut


    def Right_crutch_data_2(self, data_1, rawmsg):
        # for i in range(5):
        #     data_1[i+7] = rawmsg[i]
        data_1[7:12] = rawmsg[0:5]
        crutchOut = [0] * 6
        for i in range(0,6):
            crutchOut[i] = int.from_bytes(bytes(data_1[0+2*i:2+2*i]), byteorder='big', signed=True)
            #self.Right_crutch_data[i] = self.Right_crutch_data[i] - 2^16
            if(i<3):
                crutchOut[i] = crutchOut[i]/50
            elif(i>=3):
                crutchOut[i] = crutchOut[i]/2000
        #print("Right")
        return crutchOut



    