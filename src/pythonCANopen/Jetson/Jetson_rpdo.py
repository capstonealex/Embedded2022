from os import TMP_MAX
from sys import byteorder
import canopen
import time
import CircularBuffer
# from numpy import loadtxt
#from MLModel import MLModel
import time
import threading
from multiprocessing import Pool
from CANNetwork import CANNetwork
import keyboard

num_rpdo = 18


model_input_circular  = CircularBuffer.circularlist(2400)


Jetson = CANNetwork(66, num_rpdo, 'Jetson_66_v12.eds', model_input_circular)

Jetson.Setup()

print("CAN BUS configuration completed, Setting up RPDO...")

Jetson.Update()

#Create the intent prediction dictionary
intents = {
    "walk~fwd": 0,
    "walkFL~stand": 1
}

#Create the ML model
#myMLModel = MLModel('walk_L_ML_model.joblib','walk_L_PCA.joblib',intents)

print("Finished CAN Setup")
startTime = time.perf_counter()
while(True):
    #Perform Prediction using ML model and Exo data
    #print([model_input_circular.Data])
    if keyboard.is_pressed("q"):
        break
        
        #prediction = myMLModel.make_prediction([model_input_circular.Data])
        #print('The Prediction is:')
        #print(prediction)
Jetson.SetupHardware()
print("Time to save 1000 data points {:.4f}".format(float(time.perf_counter() -startTime)))