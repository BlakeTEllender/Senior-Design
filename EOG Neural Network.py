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

filename = "output.csv"

tblock = np.genfromtxt(filename, delimiter=',')


tdata = tblock[:, 0:-3]
print np.shape(tdata)

tags = tblock[:,-1]
print np.shape(tags)

np.random.seed(1)
# randomly initialize our weights with mean 0
syn0 = 2*np.random.random(np.shape(tdata.T)) - 1
syn1 = 2*np.random.random((np.size(tags),1)) - 1

for j in xrange(60000):

    # Feed forward through layers 0, 1, and 2
    l0 = tdata
    l1 = nonlin(np.dot(l0, syn0))
    l2 = nonlin(np.dot(l1, syn1))

    # how much did we miss the target value?
    l2_error = tags - l2
    if (j % 10000) == 0:
        print "Error:" + str(np.mean(np.abs(l2_error)))
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

