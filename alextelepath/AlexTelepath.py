from os import TMP_MAX
from alextelepath.AlexStates import AlexState, Intent
from alextelepath.CircularBuffer import CircularBuffer
from alextelepath.RepeatTimerThread import RepeatTimerThread
from alextelepath.alexml import MLAlex, ERROR_PREDICTION
import time
from .network.CANNetwork import CANNetwork

#constants 
num_rpdo = 20
node_id = 6


class AlexTelepath(object):
    """!AlexTelepath class: The main controller for AlexTelepath
    utalizes the MachineLearning classes to make predictions by using circular
    buffer object maintained by the Network classes. AlexTelepath is responsible 
    for scheduling updates to the circular buffer as well as keep track of states
    in the system (through Network class)

    """
    def __init__(self):
        """! Initializes AlexTelepath class."""
        self.model_input_circular  = CircularBuffer(2400)
        self._jetson = CANNetwork(node_id, num_rpdo, 'Jetson_66_v21.eds', self.model_input_circular)
        self._jetson.Setup()
        self._update_thread = RepeatTimerThread(0.01, self._jetson.Update)
        self._ml_model = MLAlex()
        self._last_prediction = -1
    def start(self):
        """! Starts AlexTelepath predictions"""
        print("Starting AlexTelepath ...")
        try:
            self._update_thread.start()
            while(True):
                time.sleep(1)
                if self._jetson.accept_prediction and \
                         AlexState.isStationaryState(self._jetson.current_state): #Can make a prediction
                    my_prediction = self._ml_model.make_prediction(self._jetson.current_state, [self.model_input_circular.Data])
                   
                    if self._last_prediction != my_prediction and my_prediction != ERROR_PREDICTION:
                        print("Transmit prediction", Intent(my_prediction))
                        self._jetson.transmit_prediction(my_prediction)
                        self._last_prediction = my_prediction
        except Exception as e:
            print(e) 
        finally: 
            self.stop()
    
    def stop(self): 
        """ !Should be called to stop the program. Performs cleanup."""
        if self._update_thread is not None:
            self._update_thread.cancel()
            self._update_thread = None

            
    
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