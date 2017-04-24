#This file reads the NN output in csv formatt
#Currently displays print lines noting triggers of threshold changes
import csv
import os
import time
import numpy as np
from Shuffle_Songs import music

def light():
    music()

    #def light():
    x = 0 # reference variable equal to zero
    NN = np.genfromtxt ('/home/pi/folder/NNoutput2.csv', delimiter=",")
    num = len(NN)
    NN = [row for row in NN]
    for i in range(num):
        trigger = int(NN[i][1])
        medlev = float(NN[i][2])
        if trigger == 1 and x == 0: # check if ON/OFF trigger is activated and reference variable = 0
            x = 1 #change reference variable to 1
            os.system('irsend SEND_ONCE device Key_Power')
            print "ON" #Display ON (Will be replaced with Remote Command "ON")
        elif trigger == 1 and x == 1: #check if ON/OFF trigger is activated and reference variable = 1
            x = 0 #change reference variable back to zero
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
#music()
light()
# Things to do: - Potentially integrate change of brightness into the program



