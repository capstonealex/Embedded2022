from os import TMP_MAX
from sched import scheduler
from sys import byteorder
import canopen
import CircularBuffer
# from numpy import loadtxt
from MLAlex import MLAlex
from AlexStates import AlexState
from threading import Timer
import time
from CANNetwork import CANNetwork

#constants 
num_rpdo = 20
node_id = 66

class RepeatTimerThread(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
    def pause(self):
        self.cancel()
    def restart(self):
        self.run()

class AlexTelepath(object):
#variables
    def __init__(self, node_id):
        self.model_input_circular  = CircularBuffer.circularlist(2400)
        self.Jetson = CANNetwork(node_id, num_rpdo, 'Jetson_66_v21.eds', self.model_input_circular)
        self.Jetson.Setup()
        self.thread = RepeatTimerThread(0.01, self.Jetson.Update)
        self.MLModel = MLAlex()
        self.lastPrediction = -1
    def start(self):
        print("Starting AlexTelepath prediction...")

        try:
            self.thread.start()
            while(True):
                #self.Jetson.SetupHardware()
                time.sleep(1)
                #print(self.Jetson.current_state)
                if self.Jetson.acceptPrediction and \
                         AlexState.isStationaryState(self.Jetson.current_state): #Can make a prediction
                #     #make a prediction with data 
                    my_prediction = self.MLModel.predict_state(self.Jetson.current_state, [self.model_input_circular.Data])
                    print(self.model_input_circular.Data[0:24])
                #     #my_prediction = 1
                #     #print('The Prediction is:', my_prediction)
                #     # need to create a mapping
                    if self.lastPrediction != my_prediction and my_prediction != -1:
                        print("Transmit prediction", my_prediction)
                        self.Jetson.transmit_prediction(my_prediction)
                        self.lastPrediction = my_prediction
                # else: 
                #     pass
                #     # print("Did not make prediction")
        except Exception as e:
            print("Buffer size is:", len(self.model_input_circular.Data))
            print(e) 
                
            
            self.lastState = self.Jetson.current_state
            # time.sleep(0.1)
            # if count > 1000000:
            #     break
        # self.Jetson.SetupHardware()
    def stop(self):
        if self.thread is not None:
            self.thread.cancel()
            self.thread = None

            


time.sleep(1)
                #print(self.Jets

    #Perform Prediction using ML model and Exo data
    #print([model_input_circular.Data]
        # prediction = myMLModel.make_prediction([model_input_circular.Data])
        # print('The Prediction is:')
        # print(prediction)
if __name__ == "__main__": 
    alexTelepath = AlexTelepath(node_id)
    alexTelepath.start()

    
#This intent prediction dictionary 
#maps the Machine Learning 'intent' string representations to the RobotMode representations of next state.
# intents = {
#     "walkFR~back": BKSTEP, 
#     "walkFR~fwd": NORMALWALK,
#     "walkFR~stand": FTTG, 
#     "walkFL~fwd": NORMALWALK,
#     "walkFL~stand": FTTG, 
#     "stand~back": BKSTEP, 
#     "stand~fwd": NORMALWALK,
#     "stand~sit": SITDWN
# }

# enum class RobotMode {
#     NORMALWALK, /**< 0 */
#     SITDWN,     /**< 1 */
#     STNDUP,     /**< 2 */
#     UPSTAIR,    /**< 3 */
#     DWNSTAIR,   /**< 4 */
#     TILTUP,     /**< 5 */
#     TILTDWN,    /**< 6 */
#     RAMPUP,     /**< 7 */
#     RAMPDWN,    /**< 8 */
#     BKSTEP,     /**< 9 */
#     FTTG,       /**< 10 */
#     UNEVEN,     /**< 11 */
#     INITIAL     /**< 12 */

    # Init = 0       
    # InitSitting   = 1 
    # LeftForward   = 2
    # RightForward  = 3 
    # Standing      = 4
    # Sitting       = 5  
    # SittingDown   = 6  
    # StandingUp    = 7
    # StepFirstL    = 8
    # StepFirstR    = 9   
    # StepLastL     = 10
    # StepLastR     = 11
    # StepL         = 12        
    # StepR         = 13
    # BackStepR     = 14
    # BackStepL     = 15
    # Error         = 16
# }