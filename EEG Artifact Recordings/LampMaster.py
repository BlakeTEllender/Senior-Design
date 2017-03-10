import numpy as np
import BPNN as bpn
from epoc_writer1 import Emotiv

# Meditation Lamp Master Module!!!
# Team Six
# Senior Design
# 3/5/2017

#Defining the transfer functions and their derivatives
def sgm(x, Derivative=False):
    if not Derivative:
       return 1.0 / (1.0 + np.exp(-x))
    else:
         out = sgm(x)
         return out * (1.0 - out)

# Caling Emotiv
E = Emotiv()

#Setting up the size of the network
lFuncs = [None, sgm, sgm]
#Calling BPNN
r = bpn.BackPropagationNetwork((1007,3,1),lFuncs)



#Loading Neural Network Layer weights
f1 = ['Layerweight0Med.csv']
f2 = ['Layerweight1Med.csv']

weights0 = np.genfromtxt(f1, delimiter=',')
weights1 = np.genfromtxt(f2, delimiter=',')


print weights0
print weights1


# Setting up index of items that will be replaced as the fft of the training
# set gets taken from 2D to 1D
range1 = np.arange(72)

#Getting 3 Sec Epoc
E.update_console()
epoc = E.chunk
print epoc

# Separating time and samples
sample = epoc[:, 0]
time = epoc[:, 1]

recl = time[-1]

# Number of samples taken
sample2 = sample[-1]

# Preallocating an individual training set
blocksize = np.array(14*sample2,dtype=int)

fftblock = np.zeros(blocksize)

# Average sample rate
samplerate = sample2 / recl
print samplerate


# Cutting down to just EEG Samples
epoc2 = epoc[ np.array([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                                   13, 14, 15]),:]

# FFT of the epoch
fft = np.transpose(abs(np.fft.fft(epoc2, 72)))
print np.shape(fft)
print np.shape(fftblock)

range1 = np.arange(0,71)

# Taking the fft from a 2D array to a 1D array
for i in np.arange(0, 13):
    fftblock[range1] = fft[i,:]
    range1 = range1 + 72
# Combining into training data
NNinput = fftblock


TestOutput= r.Run(NNinput)
print TestOutput