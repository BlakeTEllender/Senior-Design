# Neural Network Training Data Packager
# Senior Design 2016-2017 Team 6
# Blake T. Ellender

#Dependencies
import numpy as np


#Defining the sigmoid function and it's derivative
def nonlin(x, deriv=False):
    if (deriv==True):
        return x*(1 - x)

    return 1/(1+np.exp(-x))

# Grabbing data from csv file
# Temporarily commented out for testing

# filename=input_raw("What is the address of the CSV would you like to train
# the network with?("No need to add quotation marks around the entry.)")



# Temporary file name variable for testing

# Loop to train multiple files
filenames1 = ["eyeblink_1_30sec", "eyeblink_2_30sec","eyeblink_3_30sec",
              "EMG_1_30sec","EMG_2_30sec","EMG_3_30sec","rock_1_30sec","rock_2_30sec","rock_3_30sec","rock_4_30sec",
             "rock_5_30sec"]
filenames =  [ s + "_Tblock.csv" for s in filenames1]
tblockc = np.ones((1,1007))
tagsb = 0

for filename in filenames:

    tblocka = np.genfromtxt(filename, delimiter=',')
    tblockb = tblocka[:, 0:-3]
    tblockc = np.vstack((tblockb,tblockc))
    tagsa = tblocka[:,-2]
    print tagsa
    tagsb = np.hstack((tagsa,tagsb))
    print tagsb

print np.shape(tagsb)
print np.shape(tblockc)


np.random.seed(1)
# randomly initialize our weights with mean 0
syn0 = 2*np.random.random(np.shape(tblockc.T)) - 1
syn1 = 2*np.random.random((np.size(tagsb),1)) - 1

for j in xrange(600000):

    # Feed forward through layers 0, 1, and 2
    l0 = tblockc
    l1 = nonlin(np.dot(l0, syn0))
    l2 = nonlin(np.dot(l1, syn1))

    # how much did we miss the target value?
    l2_error = tagsb - l2
    if (j % 10000) == 0:
        print "Error:" + str(np.mean(np.abs(l2_error))*100)
    # in what direction is the target value?
    # were we really sure? if so, don't change too much.
    l2_delta = np.dot(l2_error,nonlin(l2, deriv=True))
    # how much did each l1 value contribute to the l2 error (according to the weights)?

    l1_error = l2_delta.dot(syn1.T)
    # in what direction is the target l1?
    # were we really sure? if so, don't change too much.
    l1_delta = l1_error * nonlin(l1, deriv=True)

    syn0 += l0.T.dot(l1_delta)
    syn1 += l1.dot(l2_delta)

