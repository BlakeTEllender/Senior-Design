import epoc_writer_working_windows
from epoc_writer_working_windows import Emotiv
import time


#test program to collect data in lists and add to csv
#
epoc = Emotiv()
while True:
    print 'prebutts'
    epoc.update_console()
    x = epoc.doy
    print "butts"
    print x



