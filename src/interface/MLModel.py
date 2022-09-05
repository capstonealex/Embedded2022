import pandas as pd
import numpy as np
from numpy import loadtxt
from sklearn.decomposition import PCA
from joblib import dump, load
#print("every module imported")

class MLModel(object):
    def __init__(self, mlFileName, pcaFileName, intentsDic):
        """Initialization (loading) of the models"""
        self.mlModel = load(mlFileName)
        self.pcaModel=load(pcaFileName)
        self.intentsDictionary=intentsDic


    def __make_prediction__(self, data):
        """Perform Prediction using ML model and Exo data"""
        intent_predict_proba = self.mlModel.predict_proba(self.pcaModel.transform(data))

        # Order priority list from exoskeleton data to get intent for next movement
        # Create tuples of probability of class and class and add to a list
        prob_class_list = []
        for c in range(0,len(intent_predict_proba)):
            prob_class = (intent_predict_proba[c], self.mlModel.classes_[c])
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
        print('Priority list output in string:')
        for i in range(0,len(prob_class_list)):
           print(get_key(prob_class_list[i][1]))

        return get_key(prob_class_list[0][1])