import emotiv_linux_setup22222
from emotiv_linux_setup22222 import Emotiv
import time


#test program to collect data in lists and add to csv
#
epoc = Emotiv(3)
while True:
    epoc.update_console()
    x = epoc.doy
    print x
    
