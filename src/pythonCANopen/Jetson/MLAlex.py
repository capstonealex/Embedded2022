

class MLAlex(object):
    def __init__(self):
        """Initialization (loading) of the ML models for each state"""
        self.intents_walkL = {"walkFL~fwd": 0, "walkFL~stand": 1}
        self.intents_walkR = {"walkFR~back": 0, "walkFR~fwd": 1, "walkFR~stand": 2}
        self.intents_stand = {"stand~back": 0, "stand~fwd": 1, "stand~sit": 2}
        self.walkLModel = MLModel('walk_L_ML_model.joblib','walk_L_PCA.joblib',self.intents_walkL)
        self.walkRModel = MLModel('walk_R_ML_model.joblib','walk_R_PCA.joblib',self.intents_walkR)
        self.standModel = MLModel('stand_ML_model.joblib','walk_L_PCA.joblib',self.standModel)

    def make_prediction(self, currentState):
        """Perform Prediction using ML model and Exo data"""
        data_PCA = self.pcaModel.transform(data)
        intent_predict_proba = self.mlModel.predict_proba(data_PCA) 
        #print('Prediction probability: {}'.format(intent_predict_proba))

        # Order priority list from exoskeleton data to get intent for next movement
        # Create tuples of probability of class and class and add to a list
        prob_class_list = []
        for c in range(0,len(intent_predict_proba[0])):
            prob_class = (intent_predict_proba[0][c], self.mlModel.classes_[c])
            prob_class_list.append(prob_class)
        #print('Probability list unsorted: {}'.format(prob_class_list))

        # Sort the priority list in descending order
        prob_class_list.sort(reverse=True)

        #Output the prediction as a string
        def get_key(val):
            for key, value in self.intentsDictionary.items():
                if val == value:
                    return key
            return "key doesn't exist"

        #Output priority list in intent names
        #print('Priority list output in string:')
        #for i in range(0,len(prob_class_list)):
        #   print(get_key(prob_class_list[i][1]))

        return get_key(prob_class_list[0][1])