# This class creates a prediction model consisting of a Machine Learning joblib object,
# a Principle Componenent Analysis joblib object and an Intent Dictionary.
# The make_prediction method predicts the next exo state based one full test data set 

from joblib import load
import warnings 
warnings.filterwarnings("ignore", category=UserWarning)

class MLModel(object):
    def __init__(self, mlFileName, pcaFileName,scalerFileName,intentsDic):
        """Initialization (loading) of the models"""
        self.mlModel = load(mlFileName)
        self.pcaModel = load(pcaFileName)
        self.standardScaler = load(scalerFileName)
        self.intentsDictionary = intentsDic


    def make_prediction(self, data):
        """Perform Prediction using ML model and Exo data"""
        try:
            dataScaled = self.standardScaler.transform(data)
            print(dataScaled[0:24])
            data_PCA = self.pcaModel.transform(dataScaled)
            intent_predict_proba = self.mlModel.predict_proba(data_PCA) 
            #print(intent_predict_proba)
            #print(self.mlModel.classes_)
            # Order priority list from exoskeleton data to get intent for next movement
            # Create tuples of probability of class and class and add to a list
            prob_class_list = []
            for c in range(0,len(intent_predict_proba[0])):
                prob_class = (intent_predict_proba[0][c], self.mlModel.classes_[c])
                prob_class_list.append(prob_class)
            print(prob_class_list)
            # Sort the priority list in descending order
            prob_class_list.sort(reverse=True)
        
            # #Output the prediction as a string
            # def get_key(val):
            #     for key, value in self.intentsDictionary.items():
            #         if val == value:
            #             return key
            #     return "key doesn't exist"
            return self.intentsDictionary[prob_class_list[0][1]]
        
        #return get_key(prob_class_list[0][1])
        except Exception as e:
            print("data size is: ",len(data))