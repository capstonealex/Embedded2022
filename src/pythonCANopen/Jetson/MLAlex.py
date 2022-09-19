from MLModel import MLModel

class MLAlex(object):
    def __init__(self):
        """Initialization (loading) of the ML models for each state"""
        self.intents_walkL = {"walkFL~fwd": 0, "walkFL~stand": 1}
        self.intents_walkR = {"walkFR~back": 0, "walkFR~fwd": 1, "walkFR~stand": 2}
        self.intents_stand = {"stand~back": 0, "stand~fwd": 1, "stand~sit": 2}
        self.walkLModel = MLModel('walk_L_ML_model.joblib','walk_L_PCA.joblib',self.intents_walkL)
        self.walkRModel = MLModel('walk_R_ML_model.joblib','walk_R_PCA.joblib',self.intents_walkR)
        self.standModel = MLModel('stand_ML_model.joblib','stand_PCA.joblib',self.intents_stand)
        

    def predict_state(self, currentState, data):
        """Perform Prediction using the correct ML model and Exo data"""
        #Create a dictionary that maps the currrent state to the corresponsing Machine Learning model
        state_dictionary = {"Left Forward": self.walkLModel, "Right Forward": self.walkRModel, "Standing": self.standModel}
        
        #Perform the machine learning predictionusing the correct model
        prediction = state_dictionary[currentState].make_prediction(data)

        return prediction