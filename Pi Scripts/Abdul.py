#Program asks for user input to determine color to shine.

import time, sys
import RPi.GPIO as GPIO
import emotiv_linux_setup_working as E


A = E.Emotiv()
B = E.EmotivPacket(1,A.sensors,A.old_model)


    



redPin = 11   #Set to appropriate GPIO
greenPin = 15 #Should be set in the 
bluePin = 13  #GPIO.BOARD format

def blink(pin):
    GPIO.setmode(GPIO.BOARD)
    
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    
def turnOff(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    
def redOn():
    blink(redPin)

def redOff():
    turnOff(redPin)

def greenOn():
    blink(greenPin)

def greenOff():
    turnOff(greenPin)

def blueOn():
    blink(bluePin)

def blueOff():
    turnOff(bluePin)

def yellowOn():
    blink(redPin)
    blink(greenPin)

def yellowOff():
    turnOff(redPin)
    turnOff(greenPin)

def cyanOn():
    blink(greenPin)
    blink(bluePin)

def cyanOff():
    turnOff(greenPin)
    turnOff(bluePin)

def magentaOn():
    blink(redPin)
    blink(bluePin)

def magentaOff():
    turnOff(redPin)
    turnOff(bluePin)

def whiteOn():
    blink(redPin)
    blink(greenPin)
    blink(bluePin)

def whiteOff():
    turnOff(redPin)
    turnOff(greenPin)
    turnOff(bluePin)
    
print("""Ensure the following GPIO connections: R-11, G-13, B-15
Colors: Red, Green, Blue, Yellow, Cyan, Magenta, and White
Use the format: color on/color off""")

def main():
    while True:
        cmd = raw_input("-->")


        if cmd == "red on":
            redOn()
        elif cmd == "red off":
            redOff()
        elif cmd == "green on":
            greenOn()
        elif cmd == "green off":
            greenOff()
        elif cmd == "blue on":
            blueOn()
        elif cmd == "blue off":
            blueOff()
        elif cmd == "yellow on":
            yellowOn()
        elif cmd == "yellow off":
            yellowOff()
        elif cmd == "cyan on":
            cyanOn()
        elif cmd == "cyan off":
            cyanOff()
        elif cmd == "magenta on":
            magentaOn()
        elif cmd == "magenta off":
            magentaOff()
        elif cmd == "white on":
            whiteOn()
        elif cmd == "white off":
            whiteOff()
        else:
            print("Not a valid command")
        
        
    return
    

main()
    
