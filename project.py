#This file reads the NN output in csv formatt
#Currently displays print lines noting triggers of threshold changes
import csv
x = 0 # reference variable equal to zero
file = open("NNouput_1.csv","rb") #read in file
data = csv.reader(file) #assign file data to variable
data = [row for row in data] #iterate through rows in data
for currentrow in range(40): #loop to read in currentrow up to 45 minutes
    trigger = int(data[currentrow][1]) #create int variable for on/ff
    medlev = float(data[currentrow][2]) #create int variable for meditation level
    if trigger == 1 and x == 0: # check if ON/OFF trigger is activated and reference variable = 0
        x = 1 #change reference variable to 1
        print "ON" #Display ON (Will be replaced with Remote Command "ON")
    elif trigger == 1 and x == 1: #check if ON/OFF trigger is activated and reference variable = 1
            x = 0 #change reference variable back to zero
            print"OFF" #Display OFF (Will be replaced with Remote Command "Off")
    elif medlev < 1.45: #Initial meditation level
        print "Beginning" # (Will be replaced with Remote Command "RED")
    elif medlev < 2.9 and medlev >= 1.45: #Meditation level progression. Based on 10.1/7 (max_level/#oflight_changes)
        print "Settling" # (Will be replaced with Remote Command "Orange")
    elif medlev < 4.34 and medlev >= 2.9:
        print "Gentle Meditation"# (Will be replaced with Remote Command "Yellow")
    elif medlev < 5.78 and medlev >= 4.34:
        print "Meditation" #(Will be replaced with Remote Command "Green")
    elif medlev < 7.23 and medlev >= 5.78:
        print "Deep Meditation" # (Will be replaced with Remote Command "Blue")
    elif medlev < 8.68 and medlev >= 7.23:
        print "Deeper Meditiation" #(Will be replaced with Remote Command "Purple")
    elif medlev >= 8.68:
        print "Deepest Meditiation" # (Will be replaced with Remote Command "White")

# Things to do: -Transfer code to Raspberry PI home/testfile.py which activates upon start up
#               -Change print lines with Approapriate IRSEND Remote Command
#               -Test various meditaiton session lengths
#               -Prompt user to enter how many minutes their meditation was: lines = (minutes*60)/3
#                or have program read [last line][Column 1] for the time values lines = time/3
#                putting the lines value into the foor loop on line 6
#               - Potentially integrate change of brightness into the program
