import numpy as np
import random
import time
import math
import matplotlib.pyplot as plt
initX = 0
ux = 10
uy = 0
ax = 1
ay = 1
def getXcord(tm):
    return round((initX + (ux*tm + 0.5*ax*(tm**2))),3)

mmtNum = 35
xtrueVals = np.empty((mmtNum,0))
print(xtrueVals)
tmIv = 0.1
tmEnd = mmtNum * tmIv
itm = 0
while(itm < tmEnd):
    print(getXcord(itm))
    xtrueVals = np.append(xtrueVals, getXcord(itm))
    itm += tmIv
print(xtrueVals)
