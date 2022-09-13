from os import TMP_MAX
from sched import scheduler
from sys import byteorder
import canopen
import CircularBuffer
# from numpy import loadtxt
#from MLModel import MLModel
from threading import Timer
from CANNetwork import CANNetwork

class RepeatTimerThread(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

num_rpdo = 18


model_input_circular  = CircularBuffer.circularlist(2400)
Jetson = CANNetwork(66, num_rpdo, 'Jetson_66_v12.eds', model_input_circular)

Jetson.Setup()

thread = RepeatTimerThread(0.01, Jetson.Update)


print("CAN BUS configuration completed, waiting RPDO...")


#Create the intent prediction dictionary
intents = {
    "walk~fwd": 0,
    "walkFL~stand": 1
}
#Create the ML model
#myMLModel = MLModel('walk_L_ML_model.joblib','walk_L_PCA.joblib',intents)

# print("isPDOreceived",isPDOreceived)

thread.start()
while(True):
    #Perform Prediction using ML model and Exo data
    #print([model_input_circular.Data])
    if model_input_circular.ActualSize > 10000:
        break
        # prediction = myMLModel.make_prediction([model_input_circular.Data])
        # print('The Prediction is:')
        # print(prediction)
thread.cancel()