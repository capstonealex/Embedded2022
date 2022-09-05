


from numpy import loadtxt
from MLModel import MLModel

#Import test data
expinfo_test_original = loadtxt('dataTest.csv', delimiter=',')
expinfo_test_original = [expinfo_test_original] #required data format is 2 dimensional

#Create the intent prediction dictionary
intents = {
    "walk~fwd": 0,
    "walkFL~stand": 1
}


#Create the ML model
myMLModel = MLModel('walk_L_ML_model.joblib','walk_L_PCA.joblib',intents)


#Perform Prediction using ML model and Exo data
#expinfo_test = pca_Model.transform(expinfo_test_original)
prediction = myMLModel.make_prediction(expinfo_test_original)
print('The Prediction is:')
print(prediction)



