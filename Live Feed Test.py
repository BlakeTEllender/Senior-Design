# Live feed Test
# Senior Design 2016-2017 Team 6
# Blake T. Ellender

from emotiv2 import Emotiv

a = Emotiv()
try:
     a.setup()
except KeyboardInterrupt:
     a.close()