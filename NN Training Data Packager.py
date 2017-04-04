# Neural Network Training Data Packager
# Senior Design 2016-2017 Team 6
# Blake T. Ellender



# The purpose of this code is to take the data from the pre-processing code
# and package it for the NN Training Software.



import numpy as np
import PreFilter as PF

# Prompting user for file location



# Temporarily commented out for testing

# filenames1=input_raw("What CSVs would you like to package? Ex: EMG_2_30sec)")



# Temporary file name variable for testing
filenames1= ["base1"]
filenames =  ["Raw EEG Recordings/" + s + ".csv" for s in filenames1]
for filename in filenames:



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
    stop = 50




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

    # Array of samples may need changed
    sample = dblock2[:, 1]

    # Array of time may need changed
    time = dblock2[:, 2]

    # Recording length of total CSV file in seconds
    recl = time[-1]

    # Number of samples taken
    sample2 = sample[-1]

    # Average sample rate
    samplerate = sample2 / recl
    print samplerate

    # Selecting individual epochs
    # Preallocating an individual training set
    tset = np.zeros([14 * 40])
    o = 0
    # Preallocating the whole training data block
    tblock = np.zeros((int(stop-start-3), 560))
    # This loop creates training sets sliding along the time range given
    for n in range(start, (stop - 3)):
        # Determine what time range to pull the epoc from
        trange = np.transpose(np.where(np.logical_and(time >= n, time <= n + 3)))
        # Cutting down to just EEG Samples
        epochs = dblock2[trange, np.array([3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                                          13,14, 15, 16])]

        #epochs = dblock2[trange,np.array([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14,
        #                                 16, 17, 18])]

        # Prefiltering
        my_data = epochs
        f_fft = PF.signal.resample(my_data, 14)
        filtered = PF.bandpass(f_fft[:14, 0:40].T, 1, 30, 150, corners=1,
                            zerophase=True,
                            axis=1)  # bandpass filter, 1 is low pass freq, 30 is high pass freq, 150 is the sample rate( assumed)
        z = PF.baseline_als(filtered, 100, 0.1,
                         niter=10)  # the estmatied baseline for each channel
        bs = z - filtered  # the data with baseline correction.
        k, W, S = PF.fastica(bs, n_comp=None, algorithm='parallel', w_init=None)
        #print(S)  # The data with ICA applied





        # print np.shape(S)

        # FFT of the epoch
        fft = np.transpose(abs(np.fft.fft(S, 40)))
        # print np.shape(fft)
        # Setting up index of items that will be replaced as the fft of the training
        # set gets taken from 2D to 1D
        range1 = np.arange(40)
        # Taking the fft from a 2D array to a 1D array
        for i in np.arange(0, 13):
            tset[range1] = fft[i, :]
            range1 = range1 + 40
        # Combining into training data

        tblock[int(n-start), :] = tset
        print n
        print "s of recording being processed"
    # print epochs

    # Normalizing
    tblock = np.divide(tblock, np.amax(tblock))
    print tblock
    print np.shape(tblock)

    # Adding identifiers
    tag = np.ones(np.array([np.size(tblock,0),1]))
    med2 = np.multiply(tag, med)
    onoff2 = np.multiply(tag, onoff)
    tblock2= np.hstack((tblock,onoff2,med2))


    # Writing to CSV for NN training

    # What would you like to call this file?
    # Commented out for testing
    # output = input_raw("What would you like to name the output file? Example
    # input "
    #                  "output.csv")

    #print np.shape(tblock2)
    #print tblock2

    output = "NNTrainingBlocks/"+filename[19:-4]+"_Tblock.csv"
    np.savetxt(output, tblock2, delimiter=",")
