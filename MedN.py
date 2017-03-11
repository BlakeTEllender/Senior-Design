# Med Neural Network
# Senior Design 2016-2017 Team 6
# Blake T. Ellender

#Dependencies
import numpy as np
import BPNN
import csv


#Defining the transfer functions and their derivatives
def sgm(x, Derivative=False):
    if not Derivative:
       return 1.0 / (1.0 + np.exp(-x))
    else:
         out = sgm(x)
         return out * (1.0 - out)

def linear(x, Derivative=False):
    if not Derivative:
        return x
    else:
        return 1.0

def gaussian(x, Derivative=False):
    if not Derivative:
        return np.exp(-x ** 2)
    else:
        return -2 * x * np.exp(-x ** 2)

def tanh(x, Derivative=False):
    if not Derivative:
        return np.tanh(x)
    else:
        return 1.0 - np.tanh(x) ** 2

def truncLinear(x, Derivative=False):
    if not Derivative:
        y = x.copy()
        y[y < 0] = 0
        return y
    else:
        return 1.0


# Grabbing data from csv file
# Temporarily commented out for testing

# filename=input_raw("What is the address of the CSV would you like to train
# the network with?("No need to add quotation marks around the entry.)")

# Loop to train multiple files
#filenames1 = ["eyeblink_1_30sec", "eyeblink_2_30sec","eyeblink_3_30sec",
#             "EMG_1_30sec","EMG_2_30sec","EMG_3_30sec","meditation1",
#             "meditation2", "blink _1_60sec", "blink_2_60sec",
#             "blink_3_60sec", "baseline_2", "baseline_3"]

filenames1 = ["\EMG_1_30sec", "\eyeblink_1_30sec", "\meditation2",
              "aseline_2"]


filenames =  ["C:\Users\Blake\Documents\GitHub\Senior-Design"
              "\EMG_1_30sec_Tblock.csv",
              "C:\Users\Blake\Documents\GitHub\Senior-Design"
              "\EMG_1_30sec_Tblock.csv",
              "C:\Users\Blake\Documents\GitHub\Senior-Design"
              "\EMG_1_30sec_Tblock.csv",
              "C:\\Users\\Blake\\Documents\\GitHub\\Senior-Design"
              "\\baseline_2_Tblock.csv"]
tblockc = np.ones((1,1007))
tagsb = 0

for s in filenames:

    tblocka = np.genfromtxt(s, delimiter=',')
    print np.shape(tblocka)
    tblockb = tblocka[:, 0:-3]
    tblockc = np.vstack((tblockb,tblockc))
    tagsa = tblocka[:,-1]

    tagsb = np.hstack((tagsa,tagsb))
print tagsb




lvInput = tblockc
lvTarget = tagsb.T
print np.shape(tblockc)
lFuncs = [None, sgm, sgm]

bpn = BPNN.BackPropagationNetwork((1007, 3, 1), lFuncs)

lnMax = 1000
lnErr = 1e-3
for i in range(lnMax + 1):
    err = bpn.TrainEpoch(lvInput, lvTarget, trainingRate=0.001, momentum=0.77)
    if i %  100== 0 and i > 0:
        print("Iteration {0:6d}  - Error: {1:0.6f}".format(int(i ),
                                                             err))
    if err <= lnErr:
        print("Desired error reached. Iter: {0}".format(i))
        break


np.savetxt('Layerweight0Med.csv', bpn.weights[0], delimiter=",")
np.savetxt('Layerweight1Med.csv', bpn.weights[1], delimiter=",")

# Testing against other data

#TestBlock2 =  'meditation1_Testblock.csv'
#TestBlock1 = np.genfromtxt(TestBlock2, delimiter=',')
#print TestBlock1
#TestBlock = TestBlock1[:, 0:-3]

#lvOutput = bpn.Run(TestBlock)

#print np.round(np.abs(lvOutput-1))
#print sum(np.round(lvOutput))
#print np.size(lvOutput)