from anyio import create_unix_listener
import numpy as np
import random
import time
import math
import matplotlib.pyplot as plt

"""

matrix
[[1        ,0        ,0        ,0        ,0        ,0],
 [0        ,1        ,0        ,0        ,0        ,0],
 [0        ,0        ,1        ,0        ,0        ,0],
 [0        ,0        ,0        ,1        ,0        ,0],
 [0        ,0        ,0        ,0        ,1        ,0],
 [0        ,0        ,0        ,0        ,0        ,1]]

state transition matrix
[[1        ,mmtTime  ,0.5*(mmtTime**2) ,0        ,0        ,0],
 [0        ,1        ,mmtTime          ,0        ,0        ,0],
 [0        ,0        ,1                ,0        ,0        ,0],
 [0        ,0        ,0                ,1        ,mmtTime  ,0.5*(mmtTime**2)],
 [0        ,0        ,0                ,0        ,1        ,mmtTime],
 [0        ,0        ,0                ,0        ,0        ,1]] 

process noise matrix
[[0.25*(mmtTime**4) ,0.5*(mmtTime**3) ,0.5*(mmtTime**2) ,0                 ,0                ,0],
 [0.5*(mmtTime**3)  ,mmtTime**2       ,mmtTime          ,0                 ,0                ,0],
 [0.5*(mmtTime**2)  ,mmtTime          ,1                ,0                 ,0                ,0],
 [0                 ,0                ,0                ,0.25*(mmtTime**4) ,0.5*(mmtTime**3) ,0.5*(mmtTime**2)],
 [0                 ,0                ,0                ,0.5*(mmtTime**3)  ,mmtTime**2       ,mmtTime],
 [0                 ,0                ,0                ,0.5*(mmtTime**2)  ,mmtTime          ,1]]

measurement uncertainty
[[mmtErrDev**2 ,0]
 [0            ,mmtErrDev**2]] 



"""


mmtTime = 1
accDev = 0.2
mmtErrDev = 3
mmtNum = 35

xTrueVals = np.array([])
yTrueVals = np.array([])
xSensorVals = np.array([])
ySensorVals = np.array([])

tmEnd = mmtNum * mmtTime
itm = 0

# Generate True Value
initX = -400
initY = 300
curX=initX
curY=initY
vel = 26
#ux = 5
#uy = 5
#ax = 2
#ay = 8
turn_radius = 300
thetaI = 1.57
thetaF = -1.57
curTheta = thetaI
delTheta = thetaI - thetaF
omega = vel/turn_radius
dTheta = omega * mmtTime


def getCoords(tm):
    global xTrueVals
    global yTrueVals
    global curX
    global curY
    global curTheta
    if(curX >= 0):
        if(curTheta >= thetaF):
            curTheta -= dTheta
            curX = turn_radius*math.cos(curTheta)
            curY = turn_radius*math.sin(curTheta)
            xTrueVals = np.append(xTrueVals, round((turn_radius*math.cos(curTheta)),3))
            yTrueVals = np.append(yTrueVals, round((turn_radius*math.sin(curTheta)),3))

    if(curX <= 0): 
        curX = initX + vel*tm 
        curY = initY
        xTrueVals = np.append(xTrueVals, round((initX + vel*tm),3))
        yTrueVals = np.append(yTrueVals, round(initY,3))
    #return round((initX + (ux*tm + 0.5*ax*(tm**2))),3)

def generateData(mtime, stdDev, mnum):
    global itm
    global mmtTime 
    global mmtErrDev
    global mmtNum
    global tmEnd
    global xSensorVals
    global ySensorVals

    mmtTime = mtime
    mmtErrDev = stdDev
    mmtNum = mnum
    tmEnd = mmtNum * mmtTime
    while(itm < tmEnd):
        getCoords(itm)
        itm += mmtTime
    xnoise = np.random.normal(0, mmtErrDev, xTrueVals.shape)
    ynoise = np.random.normal(0, mmtErrDev, yTrueVals.shape)
    xSensorVals = xTrueVals + xnoise
    ySensorVals = yTrueVals + xnoise


