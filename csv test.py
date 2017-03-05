import numpy as np

TestBlock2 =  'meditation1_Testblock.csv'
TestBlock1 = np.genfromtxt(TestBlock2, delimiter=',', skip_header=1)
print TestBlock1
#TestBlock = TestBlock1[:, 0:-3]