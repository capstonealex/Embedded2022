from curses import ERR
from .MLModel import MLModel
from alextelepath.AlexStates import AlexState, Intent
from alextelepath.alexml.MLPredictionClass import MLPredictionClass

ERROR_PREDICTION = -1

class MLAlex(MLPredictionClass):
    """MLAlex class: specific implementation of 2021 R&D model
    
    Inherits from superclass IMLModel
    """
    def __init__(self):
        # """Initialization (loading) of the ML models for each state"""
        self.intents_walkL = { 0: "walkFL~fwd", 1: "walkFL~stand"}
        self.intents_walkR = { 0: "walkFR~back", 1: "walkFR~fwd", 2: "walkFR~stand"}
        self.intents_stand = { 0: "stand~back", 1: "stand~fwd"}
        self.crutch_intent = {"walkFR~fwd" : Intent.FTTG, "walkFR~stand": Intent.FTTG, "walkFL~fwd":Intent.NORMALWALK, \
            "walkFL~stand": Intent.FTTG, "walkFR~back": Intent.BKSTEP, "stand~back": Intent.BKSTEP, "stand~fwd": Intent.NORMALWALK}
        self.walkLModel = MLModel('walk_L_ML_model_sklrn_1_0_2.joblib','walk_L_PCA_sklrn_1_0_2.joblib' , \
            'walk_L_SC.joblib',self.intents_walkL)
        self.walkRModel = MLModel('walk_R_ML_model_sklrn_1_0_2.joblib','walk_R_PCA_sklrn_1_0_2.joblib', \
            'walk_R_SC.joblib',self.intents_walkR)
        self.standModel = MLModel('stand_ML_model_sklrn_1_0_2.joblib','stand_PCA_sklrn_1_0_2.joblib',\
            'stand_SC.joblib', self.intents_stand)    
        # self.walkLModel = MLModel('walk_L_ML_model_sklrn_1_0_2.joblib','walk_L_PCA.joblib',self.intents_walkL)
        # self.walkRModel = MLModel('walk_R_ML_model.joblib','walk_R_PCA.joblib',self.intents_walkR)
        # self.standModel = MLModel('stand_ML_model.joblib','stand_PCA.joblib',self.intents_stand)  
        # #Create a dictionary that maps the currrent state to the corresponsing Machine Learning model
        self.state_dictionary = {AlexState.LeftForward: self.walkLModel, AlexState.RightForward: self.walkRModel, AlexState.Standing: self.standModel}

    def make_prediction(self, currentState, data):
        """Perform Prediction using the correct ML model and Exo data"""
        if currentState not in self.state_dictionary.keys():
            return ERROR_PREDICTION
        
        prediction = self.state_dictionary[currentState].make_prediction(data)
        pdo_prediction = int(self.crutch_intent[prediction])
        return pdo_prediction
    