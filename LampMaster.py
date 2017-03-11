import numpy as np
import BPNN as bpn
import MedN

# Meditation Lamp Master Module!!!
# Team Six
# Senior Design
# 3/5/2017

from epoc_writer1 import Emotiv

# Defining the transfer functions and their derivatives
def sgm(x, Derivative=False):
    if not Derivative:
        return 1.0 / (1.0 + np.exp(-x))
    else:
        out = sgm(x)
        return out * (1.0 - out)


# Caling Emotiv
E = Emotiv()

# Setting up the size of the network
lFuncs = [None, sgm, sgm]
# Calling BPNN
r = bpn.BackPropagationNetwork((1007, 3, 1), lFuncs)

# Loading Neural Network Layer weights Layerweight0Med.csv

weights0 = np.genfromtxt(
    'C:\Users\Blake\Documents\GitHub\Senior-Design\Layerweight0Med.csv',
    delimiter=",")
weights1 = np.genfromtxt(
    'C:\Users\Blake\Documents\GitHub\Senior-Design\Layerweight1Med.csv',
    delimiter=',')

# Setting up index of items that will be replaced as the fft of the training
# set gets taken from 2D to 1D
range1 = np.arange(72)

# Getting 3 Sec Epoc
E.update_console()
epoc = E.chunk

# Separating time and samples
sample = epoc[:, 0]
time = epoc[:, 1]

#Recording length
recl = time[-1]

# Number of samples taken
sample2 = sample[-1]

# Preallocating an individual training set
fftblock = np.zeros(1008)

# Average sample rate
samplerate = sample2 / recl
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

# Combining into training data

print MedN.bpn.Run(fftblock)

# print np.shape(fftblock)
# print np.shape(weights0)
# print np.shape(weights1)
# r.weights[0]=weights0
# r.weights[1]=weights1

# TestOutput = r.Run(fftblock)
