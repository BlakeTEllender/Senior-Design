# Meditation Lamp Master Module!!!
# Team Six
# Senior Design
# 3/5/2017

from csv_writer_loop import Emotiv
import numpy as np



# Defining the transfer function
def sgm(x, Derivative=False):
    if not Derivative:
        return 1.0 / (1.0 + np.exp(-x))
    else:
        out = sgm(x)
        return out * (1.0 - out)


# Caling Emotiv
E = Emotiv()


# Loading Neural Network Layer weights

weights0Med = np.genfromtxt(
    'C:\Users\Blake\Documents\GitHub\Senior-Design\Layerweight0Med.csv',
    delimiter=",")
weights1Med = np.genfromtxt(
    'C:\Users\Blake\Documents\GitHub\Senior-Design\Layerweight1Med.csv',
    delimiter=',')
weights0OnOff = np.genfromtxt(
    'C:\Users\Blake\Documents\GitHub\Senior-Design\Layerweight0OnOff.csv',
    delimiter=",")
weights1OnOff = np.genfromtxt(
    'C:\Users\Blake\Documents\GitHub\Senior-Design\Layerweight1OnOff.csv',
    delimiter=',')
# Setting up index of items that will be replaced as the fft of the training
# set gets taken from 2D to 1D
range1 = np.arange(72)

# Setting up value for temporal addition of meditation level
lastiteration = 0


# 30 minute session loop




# Getting 3 Sec Epoc
a = Emotiv()
a.setup()

epoc = np.genfromtxt(
    'C:\Users\Blake\Documents\GitHub\Senior-Design\holder1.csv',
    delimiter=',')

print epoc



# Preallocating an individual training set
fftblock = np.zeros((1008))

# Separating time and samples
samples = epoc[:, 0]
time = epoc[:, 1]


# Number of samples taken
sample2 = samples[-1]



# Average sample rate
samplerate = sample2 / 3
print "Sample Rate"
print samplerate

# Cutting down to just EEG Samples
epoc2 = epoc[np.array([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                       13, 14, 15]), :]

# FFT of the epoch
fft = np.transpose(abs(np.fft.fft(epoc2, 72)))


range1 = np.arange(0, 71)

# Taking the fft from a 2D array to a 1D array
for i in np.arange(0, 13):
    fftblock[range1] = fft[i, :]
    range1 = range1 + 72

# Adding ones layer
fftblock = np.vstack([fftblock, np.ones([1,1008])])

#Pushing through Meditation NN
l0 = fftblock
l1m = sgm(np.dot(l0, weights0Med.T))
l2m = sgm(np.dot(np.hstack([l1m, np.ones([2, 1])]), weights1Med))

#Pushing through OnOff NN
l1O = sgm(np.dot(l0, weights0OnOff.T))
l2O = sgm(np.dot(np.hstack([l1m, np.ones([2, 1])]), weights1OnOff))
MLevel = (l2m[0] + lastiteration)
lastiteration = l2m[0]
Output = (MLevel), (l2O[0])

print "Meditation Detected?"
print Output[0]
print "OnOff Trigger Detected?"
print Output[1]





