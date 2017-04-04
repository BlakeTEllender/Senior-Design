# Neural Network Testing Data Packager
# Senior Design 2016-2017 Team 6
# Blake T. Ellender



# The purpose of this code is to take the data from the pre-processing code
# and package it for the NN Training Software.



import numpy as np

# Prompting user for file location



# Temporarily commented out for testing

# filenames1=input_raw("What CSVs would you like to package? Ex: EMG_2_30sec)")



# Temporary file name variable for testing

filenames =  ["C:\Users\Blake\Documents\GitHub\Senior-Design\holder1.csv"]
for filename in filenames:



    # Importing as Numpy Array

    dblock = np.genfromtxt(filename, delimiter=',')
    dblock = dblock[204:-1, :]

    # Region Selection



    # At what time in the recording would you like to start the packaging the data?


    # Commented out for testing
    # start = input("At what time in the recording would you like to start  "
    #              "packaging the data? (Input in seconds.)")

    start = 1


    # Prompting the user for the end of the desired event.

    # Commented out for testing
    # stop = input("At what time in the recording would you like to stop packaging "
    #            "the data?")
    stop = 3

    # Tagging training sets for NN

    # Is this recording Meditative?
    med = input("Is " + filename + " a recording of meditation? (1/0)")

    # Is this recording and ON/OFF trigger?

    # This line is commented out for testing
    onoff = input("Is the" +filename + " a recording of an ON/OFF Signal? ("
                                       "1/0)")

    # This collects time and sample info from the CSV then culls the matrix to
    # just the eeg data.

    # Removing labels from the first row of the CSV
    dblock2 = dblock[1:, :]

    # Array of samples
    sample = dblock2[:, 1]

    # Array of time
    time = dblock2[:, 2]

    # Recording length of total CSV file in seconds
    recl = time[-1]

    # Number of samples taken
    sample2 = sample[-1]

    # Average sample rate
    samplerate = sample2 / recl

    # Selecting individual epochs
    # Preallocating an individual testing set
    tset = np.zeros([14 * 72])

    # Preallocating the whole testing data block
    tbsets = np.arange(stop-start-3)
    tblock = np.zeros((stop-start-3, 1008))

    # This loop creates testing sets sliding along the time range given


    for n in tbsets:
        # Determine what time range to pull the epoc from
        trange = np.transpose(np.where(np.logical_and(time >= n, time <= n + 3)))
        # Cutting down to just EEG Samples

        epochs = dblock2[trange, np.array([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                                           13, 14, 15])]
        # FFT of the epoch
        fft = np.transpose(abs(np.fft.fft(epochs, 72)))

        # Setting up index of items that will be replaced as the fft of the training
        # set gets taken from 2D to 1D
        range1 = np.arange(72)
        # Taking the fft from a 2D array to a 1D array
        for i in np.arange(0, 13):
            tset[range1] = fft[i, :]
            range1 = range1 + 72
        # Combining into training data
        tblock[n,:] = tset


    # Normalizing
    tblock = tblock / np.amax(tblock)

    # Adding identifiers
    tag = np.ones((stop-start-3,1))
    med2 = np.multiply(tag, med)
    onoff2 = np.multiply(tag, onoff)
    tblock2= np.hstack((tblock,onoff2,med2))


    # Writing to CSV for NN testing

    # What would you like to call this file?
    # Commented out for testing
    # output = input_raw("What would you like to name the output file? Example
    # input "
    #                  "output.csv")

    print np.shape(tblock2)

    print tblock2


    np.savetxt("OnOff_TBlock.csv", tblock2, delimiter=',')
