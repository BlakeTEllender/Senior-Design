import epoc_writer1
from epoc_writer1 import Emotiv
import time


#test program to collect data in lists and add to csv
#
epoc = Emotiv(3)
while True:
    print 'prebutts'
    epoc.update_console()
    x = epoc.doy
    print "butts"
    print x



