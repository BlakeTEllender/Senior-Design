# Neural Network Training Data Packager
# Senior Design 2016-2017 Team 6
# Blake T. Ellender



# The purpose of this code is to take the data from the pre-processing code
# and package it for the NN Training Software.



import numpy as np

# Prompting user for file location



# Temporarily commented out for testing

# filename=input_raw("What is the address of the CSV would you like to package?("
#                   "No need to add"
#                   "quotation marks around the entry.)")



# Temporary file name variable for testing

filename = "C:\EEG Artifact Recordings\eyeblink_2_30sec.csv"

# Importing as Numpy Array

dblock = np.genfromtxt(filename, delimiter=',')

# Region Selection



# At what time in the recording would you like to start the packaging the data?


# Commented out for testing
# start = input("At what time in the recording would you like to start  "
#              "packaging the data? (Input in seconds.)")

start = 10

# Prompting the user for the end of the desired event.

# Commented out for testing
# stop = input("At what time in the recording would you like to stop packaging "
#            "the data?")
stop = 20

# Tagging training sets for NN

# Is this recording Meditative?


# This line is commented out for testing
# med = input("Is this recording Meditative? (1/0)")

med = 0

# Is this recording and ON/OFF trigger?

# This line is commented out for testing
# onoff = input("Is this recording Meditative? (1/0)")

onoff = 1

# This collects time and sample info from the CSV then culls the matrix to
# just the eeg data.

# Removing labels from the first row of the CSV
dblock2 = dblock[1:, :]

# Array of samples
sample = dblock2[:, 0]

# Array of time
time = dblock2[:, 1]

# Recording length of total CSV file in seconds
recl = time[-1]

# Number of samples taken
sample2 = sample[-1]

# Average sample rate
samplerate = sample2 / recl

# Selecting individual epochs
# Preallocating an individual training set
tset = np.zeros([14 * 72])

# Preallocating the whole training data block
tbsets = stop - start - 3
tblock = np.zeros((tbsets, 1008))

# This loop creates training sets sliding along the time range given


for n in np.arange(0, tbsets):
    # Determine what time range to pull the epoc from
    trange = np.transpose(np.where(np.logical_and(time >= n, time <= n + 3)))
    # Cutting down to just EEG Samples
    epochs = dblock2[trange, np.array([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14,
                                       16, 17, 18])]
    # FFT of the epoch
    fft = np.transpose(abs(np.fft.fft(epochs, 72, 0)))
    # Setting up index of items that will be replaced as the fft of the training
    # set gets taken from 2D to 1D
    range1 = np.arange(72)
    # Taking the fft from a 2D array to a 1D array
    for i in np.arange(0, 13):
        tset[range1] = fft[i, :]
        range1 = range1 + 72
    # Combining into training data
    tblock[n, :] = tset

print np.shape(fft)

# Normalizing
tblock = tblock / np.amax(tblock)

# Adding identifiers
tag = np.ones((tbsets,1))
print np.size(tag)
med2 = np.multiply(tag, med)
onoff2 = np.multiply(tag, onoff)
tblock2= np.hstack((tblock,onoff2,med2))


# Writing to CSV for NN training

# What would you like to call this file?
# Commented out for testing
# output = input_raw("What would you like to name the output file? Example
# input "
#                  "output.csv")
output = "output.csv"
np.savetxt(output, tblock2, delimiter=",")
