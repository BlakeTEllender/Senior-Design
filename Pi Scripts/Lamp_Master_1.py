# Meditation Lamp Master Module!!!
# Team Six
# Senior Design
# 3/5/2017

from csv_writer_loop_linux import Emotiv
import numpy as np
import csv
import os
import time
from Shuffle_Songs import music
music()
Ziggy = 0
os.system('irsend SEND_ONCE device Key_U')



# Defining the transfer function
def sgm(x, Derivative=False):
    if not Derivative:
        return 1.0 / (1.0 + np.exp(-x))
    else:
        out = sgm(x)
        return out * (1.0 - out)


# Caling Emotiv



# Loading Neural Network Layer weights
weights0Med = np.genfromtxt(
    '/home/pi/Downloads/Senior-Design-master/LayerWeights/Layerweight0Med.csv',
    delimiter=",")
weights1Med = np.genfromtxt(
    '/home/pi/Downloads/Senior-Design-master/LayerWeights/Layerweight1Med.csv',
    delimiter=',')
weights0OnOff = np.genfromtxt(
    '/home/pi/Downloads/Senior-Design-master/LayerWeights/Layerweight0OnOff.csv',
    delimiter=",")
weights1OnOff = np.genfromtxt(
    '/home/pi/Downloads/Senior-Design-master/LayerWeights/Layerweight1OnOff.csv',
    delimiter=',')
# Setting up index of items that will be replaced as the fft of the training
# set gets taken from 2D to 1D
range1 = np.arange(72)

# Setting up value for temporal addition of meditation level
lastiteration = 0


# 30 minute session loop


for x in xrange(1,600):
    clear = []
    np.savetxt('holder1.csv', clear, delimiter=",")
    # Getting 3 Sec Epoch
    A = Emotiv()
    A.setup()
    A.close()
    
    
    

    epoc = np.genfromtxt(
        '/home/pi/folder/holder1.csv',
        delimiter=',')




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
    epoc2 = epoc[np.array([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]), :]
                           

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
    l2O = sgm(np.dot(np.hstack([l1O, np.ones([2, 1])]), weights1OnOff))
    MedLevel = l2m[0] + lastiteration
    Output = (MedLevel), (l2O[0])
    trigger = Output[1]
    medlev = Output[0]

    if trigger >= .5 and Ziggy == 0: # check if ON/OFF trigger is activated and reference variable = 0
        Ziggy = 1 #change reference variable to 1
        os.system('irsend SEND_ONCE device Key_Power')
        print "ON" #Display ON (Will be replaced with Remote Command "ON")
    elif trigger >= .5 and Ziggy == 1: #check if ON/OFF trigger is activated and reference variable = 1
        Ziggy = 0 #change reference variable back to zero
        os.system('irsend SEND_ONCE device Key_U')
        print"OFF" #Display OFF (Will be replaced with Remote Command "Off")
    elif medlev < 1.45: #Initial meditation level
        os.system('irsend SEND_ONCE device Key_RED')
        print "Beginning" # (Will be replaced with Remote Command "RED")
    elif medlev < 2.9 and medlev >= 1.45: #Meditation level progression. Based on 10.1/7 (max_level/#oflight_changes)
        os.system('irsend SEND_ONCE device BTN_3')
        print "Settling" # (Will be replaced with Remote Command "Orange")
    elif medlev < 4.34 and medlev >= 2.9:
        os.system('irsend SEND_ONCE device BTN_6')
        print "Gentle Meditation"# (Will be replaced with Remote Command "Yellow")
    elif medlev < 5.78 and medlev >= 4.34:
        os.system('irsend SEND_ONCE device Key_Green')
        print "Meditation" #(Will be replaced with Remote Command "Green")
    elif medlev < 7.23 and medlev >= 5.78:
        os.system('irsend SEND_ONCE device Key_Blue')
        print "Deep Meditation" # (Will be replaced with Remote Command "Blue")
    elif medlev < 8.68 and medlev >= 7.23:
        os.system('irsend SEND_ONCE device BTN_8')
        print "Deeper Meditiation" #(Will be replaced with Remote Command "Purple")
    elif medlev >= 8.68:
        os.system('irsend SEND_ONCE device Key_V')
        print "Deepest Meditiation" # (Will be replaced with Remote Command "White")


    print "Meditation Detected?"
    print Output[0]
    print "OnOff Trigger Detected?"
    print Output[1]
    print "Iteration"
    print x

 
