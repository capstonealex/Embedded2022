from MLModel import MLModel
from enum import IntEnum
class State(IntEnum):
    LeftForward = 2
    RightForward = 3
    Standing = 4
class Intent(IntEnum):
    NORMALWALK = 0
    FTTG = 10
    BKSTEP = 9
    SITDOWN = 1
# "walkFR~back": BKSTEP, 
#     "walkFR~fwd": NORMALWALK,
#     "walkFR~stand": FTTG, 
#     "walkFL~fwd": NORMALWALK,
#     "walkFL~stand": FTTG, 
#     "stand~back": BKSTEP, 
#     "stand~fwd": NORMALWALK,
#     "stand~sit": SITDWN
# }

class MLAlex(object):
    def __init__(self):
        """Initialization (loading) of the ML models for each state"""
        self.intents_walkL = { 0: "walkFL~fwd", 1: "walkFL~stand"}
        self.intents_walkR = { 0: "walkFR~back", 1: "walkFR~fwd", 2: "walkFR~stand"}
        self.intents_stand = { 0: "stand~back", 1: "stand~fwd", 2: "stand~sit" }
        self.crutch_intent = {"walkFR~fwd" : Intent.BKSTEP, "walkFR~stand": Intent.FTTG, "walkFL~fwd":Intent.NORMALWALK, \
            "walkFL~stand": Intent.FTTG, "stand~back": Intent.BKSTEP, "stand~fwd": Intent.NORMALWALK, "stand~sit": Intent.SITDOWN }
        self.walkLModel = MLModel('walk_L_ML_model.joblib','walk_L_PCA.joblib',self.intents_walkL)
        self.walkRModel = MLModel('walk_R_ML_model.joblib','walk_R_PCA.joblib',self.intents_walkR)
        self.standModel = MLModel('stand_ML_model.joblib','stand_PCA.joblib',self.intents_stand)      

    def predict_state(self, currentState, data):
        """Perform Prediction using the correct ML model and Exo data"""
        #Create a dictionary that maps the currrent state to the corresponsing Machine Learning model
        state_dictionary = {State.LeftForward: self.walkLModel, State.RightForward: self.walkRModel, State.Standing: self.standModel}
        # Perform the machine learning predictionusing the correct model
        if currentState in state_dictionary.keys():
            prediction = state_dictionary[currentState].make_prediction(data)
            pdo_prediction = self.crutch_intent.get(prediction).value
        else:
            print("Not a valid prediction state.")
            return "invalid"
        return pdo_prediction