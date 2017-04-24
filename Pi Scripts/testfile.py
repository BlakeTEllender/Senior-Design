#This file reads the NN output in csv formatt
#Currently displays print lines noting triggers of threshold changes
import csv
import os
import pygame
pygame.mixer.init()
pygame.mixer.music.load('/home/pi/Downloads/meditation1.mp3')
pygame.mixer.music.play()
while pygame.mixer.music.get_busy(): 
    x = 0 # reference variable equal to zero
    os.system('irsend SEND_ONCE device Key_U') #Default light off before beginning
    filename = 'NNoutput2.csv'
    num_lines = len(open(filename).readlines()) #Calculate number of rows in CSV file
    file = open(filename,"rb") #read in file
    data = csv.reader(file) #assign file data to variable
    data = [row for row in data] #iterate through rows in data
    for currentrow in range(num_lines): #loop to read in currentrow up to 45 minutes
        trigger = int(data[currentrow][1]) #create int variable for on/ff
        medlev = float(data[currentrow][2]) #create int variable for meditation level
        if trigger == 1 and x == 0: # check if ON/OFF trigger is activated and reference variable = 0
            x = 1 #change reference variable to 1
            os.system('irsend SEND_ONCE device Key_Power')
            print "ON" #Display ON (Will be replaced with Remote Command "ON")
        elif trigger == 1 and x == 1: #check if ON/OFF trigger is activated and reference variable = 1
            x = 0 #change reference variable back to zero
            os.system('irsend SEND_ONCE device Key_U')
            print"OFF" #Display OFF (Will be replaced with Remote Command "Off")
        
        elif medlev < .36: #Initial meditation level
            os.system('irsend SEND_ONCE device Key_RED')
            os.system('irsend SEND_ONCE device Key_T') #Lowest brightness
            os.system('irsend SEND_ONCE device Key_T')
            os.system('irsend SEND_ONCE device Key_T')
            print "Beginning" # (Will be replaced with Remote Command "RED")
        elif medlev < .72 and medlev >= .36:
            os.system('irsend SEND_ONCE device Key_TV') #Increase brightness
        elif medlev < 1.08 and medlev >= .72:
            os.system('irsend SEND_ONCE device Key_TV') #Increase brightness
        elif medlev < 1.45 and medlev >= 1.08:
            os.system('irsend SEND_ONCE device Key_TV') #Increase brightness
        
        elif medlev < 1.81 and medlev >= 1.45: #Meditation level progression. Based on 10.1/7 (max_level/#oflight_changes)
            os.system('irsend SEND_ONCE device BTN_3')
            os.system('irsend SEND_ONCE device Key_T') #Lowest brightness
            os.system('irsend SEND_ONCE device Key_T')
            os.system('irsend SEND_ONCE device Key_T')
            print "Settling" # (Will be replaced with Remote Command "Orange")
        elif medlev < 2.17 and medlev >= 1.81:
            os.system('irsend SEND_ONCE device Key_TV') #Increase brightness
        elif medlev < 2.53 and medlev >= 2.17:
            os.system('irsend SEND_ONCE device Key_TV') #Increase brightness
        elif medlev < 2.9 and medlev >= 2.53:
            os.system('irsend SEND_ONCE device Key_TV') #Increase brightness
            
        elif medlev < 3.26 and medlev >= 2.9:
            os.system('irsend SEND_ONCE device BTN_6')
            os.system('irsend SEND_ONCE device Key_T') #Lowest brightness
            os.system('irsend SEND_ONCE device Key_T')
            os.system('irsend SEND_ONCE device Key_T')
            print "Gentle Meditation"# (Will be replaced with Remote Command "Yellow")
        elif medlev < 3.62 and medlev >= 3.26:
            os.system('irsend SEND_ONCE device Key_TV') #Increase brightness
        elif medlev < 3.98 and medlev >= 3.62:
            os.system('irsend SEND_ONCE device Key_TV') #Increase brightness
        elif medlev < 4.34 and medlev >= 3.98:
            os.system('irsend SEND_ONCE device Key_TV') #Increase brightness
            
        elif medlev < 4.7 and medlev >= 4.34:
            os.system('irsend SEND_ONCE device Key_Green')
            os.system('irsend SEND_ONCE device Key_T') #Lowest brightness
            os.system('irsend SEND_ONCE device Key_T')
            os.system('irsend SEND_ONCE device Key_T')
            print "Meditation" #(Will be replaced with Remote Command "Green")
        elif medlev < 5.06 and medlev >= 4.7:
            os.system('irsend SEND_ONCE device Key_TV') #Increase brightness
        elif medlev < 5.42 and medlev >= 5.06:
            os.system('irsend SEND_ONCE device Key_TV') #Increase brightness
        elif medlev < 5.78 and medlev >= 5.42:
            os.system('irsend SEND_ONCE device Key_TV') #Increase brightness
            
        elif medlev < 6.14 and medlev >= 5.78:
            os.system('irsend SEND_ONCE device Key_Blue')
            os.system('irsend SEND_ONCE device Key_T') #Lowest brightness
            os.system('irsend SEND_ONCE device Key_T')
            os.system('irsend SEND_ONCE device Key_T')
            print "Deep Meditation" # (Will be replaced with Remote Command "Blue")
        elif medlev < 6.5 and medlev >= 6.14:
            os.system('irsend SEND_ONCE device Key_TV') #Increase brightness
        elif medlev < 6.86 and medlev >= 6.5:
            os.system('irsend SEND_ONCE device Key_TV') #Increase brightness
        elif medlev < 7.22 and medlev >= 6.86:
            os.system('irsend SEND_ONCE device Key_TV') #Increase brightness
            
        elif medlev < 7.58 and medlev >= 7.22:
            os.system('irsend SEND_ONCE device BTN_8')
            os.system('irsend SEND_ONCE device Key_T') #Lowest brightness
            os.system('irsend SEND_ONCE device Key_T')
            os.system('irsend SEND_ONCE device Key_T')
            print "Deeper Meditiation" #(Will be replaced with Remote Command "Purple")
        elif medlev < 7.94 and medlev >= 7.58:
            os.system('irsend SEND_ONCE device Key_TV') #Increase brightness
        elif medlev < 8.3 and medlev >= 7.94:
            os.system('irsend SEND_ONCE device Key_TV') #Increase brightness
        elif medlev < 8.66 and medlev >= 8.3:
            os.system('irsend SEND_ONCE device Key_TV') #Increase brightness
            
        elif medlev < 9.02 and medlev >= 8.66:
            os.system('irsend SEND_ONCE device Key_V')
            os.system('irsend SEND_ONCE device Key_T') #Lowest brightness
            os.system('irsend SEND_ONCE device Key_T')
            os.system('irsend SEND_ONCE device Key_T')
            print "Deepest Meditiation" # (Will be replaced with Remote Command "White")
        elif medlev < 9.38 and medlev >= 9.02:
            os.system('irsend SEND_ONCE device Key_TV') #Increase brightness
        elif medlev < 9.74 and medlev >= 9.38:
            os.system('irsend SEND_ONCE device Key_TV') #Increase brightness
        elif medlev >= 9.74:
            os.system('irsend SEND_ONCE device Key_TV') #Increase brightness

  


