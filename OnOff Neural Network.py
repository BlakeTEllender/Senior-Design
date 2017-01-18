# Neural Network Training Data Packager
# Senior Design 2016-2017 Team 6
# Blake T. Ellender

#Dependencies
import numpy as np
import BPNN


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



# Temporary file name variable for testing

# Loop to train multiple files
filenames1 = ["eyeblink_1_30sec", "eyeblink_2_30sec","eyeblink_3_30sec",
              "EMG_1_30sec","EMG_2_30sec","EMG_3_30sec"]
filenames =  [ s + "_Tblock.csv" for s in filenames1]
tblockc = np.ones((1,1007))
tagsb = 0

for filename in filenames:

    tblocka = np.genfromtxt(filename, delimiter=',')
    tblockb = tblocka[:, 0:-3]
    tblockc = np.vstack((tblockb,tblockc))
    tagsa = tblocka[:,-2]
    tagsb = np.hstack((tagsa,tagsb))


np.random.seed(1)

lvInput = tblockc
lvTarget = tagsb
lFuncs = [None, sgm, linear]

bpn = BPNN((1008, 2, 1), lFuncs)

lnMax = 50000
lnErr = 1e-6
for i in range(lnMax + 1):
    err = bpn.TrainEpoch(lvInput, lvTarget, momentum=0.7)
    if i % 1000 == 0 and i > 0:
        print("Iteration {0:6d}K - Error: {1:0.6f}".format(int(i / 1000), err))
    if err <= lnErr:
        print("Desired error reached. Iter: {0}".format(i))
        break

    # Display output

    lvOutput = bpn.Run(lvInput)
    for i in range(lvInput.shape[0]):
        print("Input: {0} Output: {1}".format(lvInput[i], lvOutput[i]))

