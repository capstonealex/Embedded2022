from os import TMP_MAX
from sys import byteorder
import canopen
import time
import CircularBuffer
# from numpy import loadtxt
from MLModel import MLModel
import time
import threading
from CANNetwork import CANNetwork

num_rpdo = 18


model_input_circular  = CircularBuffer.circularlist(2400)
Jetson = CANNetwork(66, num_rpdo, 'Jetson_66_v12.eds', model_input_circular)

Jetson.Setup()

print("CAN BUS configuration completed, waiting RPDO...")

Jetson.Update()

#Create the intent prediction dictionary
intents = {
    "walk~fwd": 0,
    "walkFL~stand": 1
}

#Create the ML model
myMLModel = MLModel('walk_L_ML_model.joblib','walk_L_PCA.joblib',intents)

# print("isPDOreceived",isPDOreceived)


while(True):
    #Perform Prediction using ML model and Exo data
    #print([model_input_circular.Data])
    if model_input_circular.ActualSize == 2400:
        prediction = myMLModel.make_prediction([model_input_circular.Data])
        print('The Prediction is:')
        print(prediction)