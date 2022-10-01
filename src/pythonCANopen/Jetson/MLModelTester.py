from MLModel import MLModel
import pandas as pd
from numpy import genfromtxt

intentdict = { 0: "walkFR~back", 1: "walkFR~fwd", 2: "walkFR~stand"}
model = MLModel('walk_R_ML_model_sklrn_1_0_2.joblib','walk_R_PCA_sklrn_1_0_2.joblib',intentdict)
#data = pd.read_csv("dataTest0.csv", delimiter=',')
data0 = genfromtxt('dataTest0.csv', delimiter=',')
data1 = genfromtxt('dataTest1.csv', delimiter=',')
# filtered = data.iloc[:, 1:-3]
# horizontal_stack =filtered.pivot()
# print(horizontal_stack)

# data1 = [5.3633,-3.3761,-87.6059,0.519295,0.34513,-0.157718,-1.4297,-1.7045,-197.6858,-0.051848,-1.646855,-0.004677,59390.0,34286.0,-10861.0,14796.0,355.0,-582.0,0.0,-1860.0,289.0,-786.0,-11.0,-50.0] * 100
# data2 = [6.4833,-3.5761,-102.7459,0.658795,0.32663,-0.124718,-1.6897,-1.1445,-210.5258,-0.055848,-1.713355,-0.001177,59388.0,34285.0,-10862.0,14794.0,-1827.0,0.0,0.0,-1150.0,282.0,-725.0,-7.0,7.0] *100
# data3 = [4.9477,-2.4787,-161.9513,1.498007,-0.100923,-0.043318,-3.2861,2.0612,-103.9502,-0.761415,-0.654175,0.055797,59375.0,34328.0,-10863.0,14795.0,161.0,0.0,0.0,-1908.0,122.0,-468.0,-61.0,132.0]*100
# data4 = [0,0,0,0,0,0,0,2.0612,-103.9502,-0.761415,-0.654175,0.055797,59375.0,34328.0,-10863.0,14795.0,161.0,0.0,0.0,-1908.0,122.0,-468.0,-61.0,132.0]*100
# data5 = [0]*2400
model.make_prediction([data0])
model.make_prediction([data1])
# model.make_prediction([data4])