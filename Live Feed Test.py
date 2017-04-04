# Live feed Test
# Senior Design 2016-2017 Team 6
# Blake T. Ellender

from save_to_csv_3_sec_epoc import Emotiv
import numpy as np

a = Emotiv()
a.setup()


epoc = np.genfromtxt('C:\Users\Blake\Documents\GitHub\Senior-Design\sec_epoc.csv', delimiter=',')

