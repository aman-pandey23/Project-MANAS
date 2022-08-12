import GenerateDataSet
import numpy as np
import random
import time
import math
import matplotlib.pyplot as plt

np.set_printoptions(suppress=True)
np.set_printoptions(precision=3)

mmtTime = 1
mmtErrDev = 3
mmtNum = 35
GenerateDataSet.generateData(mmtTime,mmtErrDev,mmtNum)

xTrueVals = GenerateDataSet.xTrueVals
yTrueVals = GenerateDataSet.yTrueVals
xSensorVals = GenerateDataSet.xSensorVals
ySensorVals = GenerateDataSet.ySensorVals

H = np.array(
    [[1,0,0,0,0,0],    
     [0,0,0,1,0,0]]
)


Xn = np.array(
    [[0],
     [0],
     [0],
     [0],
     [0],
     [0]]
)

F = np.array(
[[1        ,mmtTime  ,0.5*(mmtTime**2) ,0        ,0        ,0],
 [0        ,1        ,mmtTime          ,0        ,0        ,0],
 [0        ,0        ,1                ,0        ,0        ,0],
 [0        ,0        ,0                ,1        ,mmtTime  ,0.5*(mmtTime**2)],
 [0        ,0        ,0                ,0        ,1        ,mmtTime],
 [0        ,0        ,0                ,0        ,0        ,1]] 
)
Q = np.array(
[[0.25*(mmtTime**4) ,0.5*(mmtTime**3) ,0.5*(mmtTime**2) ,0                 ,0                ,0],
 [0.5*(mmtTime**3)  ,mmtTime**2       ,mmtTime          ,0                 ,0                ,0],
 [0.5*(mmtTime**2)  ,mmtTime          ,1                ,0                 ,0                ,0],
 [0                 ,0                ,0                ,0.25*(mmtTime**4) ,0.5*(mmtTime**3) ,0.5*(mmtTime**2)],
 [0                 ,0                ,0                ,0.5*(mmtTime**3)  ,mmtTime**2       ,mmtTime],
 [0                 ,0                ,0                ,0.5*(mmtTime**2)  ,mmtTime          ,1]]
)


Q =  Q * (GenerateDataSet.accDev ** 2)

R = np.array(
[[mmtErrDev**2 ,0],
 [0            ,mmtErrDev**2]] 
)

P = np.array(
[[500      ,0        ,0        ,0        ,0        ,0],
 [0        ,500      ,0        ,0        ,0        ,0],
 [0        ,0        ,500      ,0        ,0        ,0],
 [0        ,0        ,0        ,500      ,0        ,0],
 [0        ,0        ,0        ,0        ,500      ,0],
 [0        ,0        ,0        ,0        ,0        ,500]]
)

#Prediction 1
P = np.matmul(F,P)
P = np.matmul(P,F.transpose())



Kgain =  np.array([])

i = 0

zi = np.array(
[[xSensorVals[i]],
 [ySensorVals[i]]] 
)

#ITER
"""
zi = np.array([[xSensorVals[i]],
               [ySensorVals[i]]])

Kgain = np.matmul(np.matmul(P,H.transpose()),np.linalg.inv(np.matmul(np.matmul(H,P),H.transpose()) + R))

XNN = np.matmul(Kgain,np.subtract(zi,np.matmul(H,Xn)))
Xn = Xn + XNN

print(Xn)
print("___")

I = np.identity(6)
P = np.matmul(np.matmul((I - np.matmul(Kgain,H)),P),(I - np.matmul(Kgain,H)).transpose()) + np.matmul(np.matmul(Kgain,R),Kgain.transpose())


Xn = np.matmul(F,Xn)

P = np.matmul(np.matmul(F,P),F.transpose()) + Q
print(P)
"""

xFilterVals = np.array([])
yFilterVals = np.array([])


while(i < xSensorVals.size):                           #xSensorVals.size
    #Kalman Gain equation
    zi = np.array([[xSensorVals[i]],
               [ySensorVals[i]]])

    Kgain = np.matmul(np.matmul(P,H.transpose()),np.linalg.inv(np.matmul(np.matmul(H,P),H.transpose()) + R))

    XNN = np.matmul(Kgain,np.subtract(zi,np.matmul(H,Xn)))
    Xn = Xn + XNN
    if(xFilterVals.size <= mmtNum):
        xFilterVals = np.append(xFilterVals,Xn[0])
    if(yFilterVals.size <= mmtNum):
        yFilterVals = np.append(yFilterVals,Xn[3])

    I = np.identity(6)
    P = np.matmul(np.matmul((I - np.matmul(Kgain,H)),P),(I - np.matmul(Kgain,H)).transpose()) + np.matmul(np.matmul(Kgain,R),Kgain.transpose())

    Xn = np.matmul(F,Xn)

    P = np.matmul(np.matmul(F,P),F.transpose()) + Q
    
    i += 1
    
print(xFilterVals)    
print(yFilterVals) 


sumdev = 0
i = 0
while(i < mmtNum):
    sumdev = sumdev + ((xFilterVals[i] - xTrueVals[i])**2 + (xFilterVals[i] - xTrueVals[i])**2)
    i = i+1
avdev = sumdev/mmtNum
dev = (avdev)**0.5
print("filter dev : ",dev)


sumdev = 0
i = 0
while(i < mmtNum):
    sumdev = sumdev + ((xSensorVals[i] - xTrueVals[i])**2 + (ySensorVals[i] - yTrueVals[i])**2)
    i = i+1
avdev = sumdev/mmtNum
stddev = (avdev)**0.5
print("sensor dev : ",stddev)


plt.xlim(-450, 350)
plt.ylim(-50, 350)
plt.gca().set_aspect('equal', adjustable='box')

plt.plot(xTrueVals, yTrueVals, marker="o", markersize=3, markerfacecolor="green")
plt.plot(xSensorVals, ySensorVals, marker="o", markersize=2, markerfacecolor="red")
plt.plot(xFilterVals, yFilterVals, marker="o", markersize=1, markerfacecolor="blue")

plt.grid()
plt.show()

