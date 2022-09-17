import GenerateDataSet as gen
import numpy as np
import random
import time
import math
import matplotlib.pyplot as plt

dataset1 = gen.CoordDataSet(1,3,50)
dataset1.generateData()

class KalmanFilter:

    xFilterVals = np.array([])
    yFilterVals = np.array([])
    

    def __init__(self, dat):
        self.dat = dat
        self.mmtTime = dat.getMmt()
        self.mmtNum = dat.getmmtNum()
        self.accDev = dat.getaccDev()
        self.mmtErrDev = dat.getstdDev()
        self.xSensorVals = dat.getxSensorVals()
        self.ySensorVals = dat.getySensorVals()
        self.H = np.array(
            [[1,0,0,0,0,0],    
             [0,0,0,1,0,0]]
        )
        self.Xn = np.array(
            [[0],
             [0],
             [0],
             [0],
             [0],
             [0]]
        )
        self.F = np.array(
        [[1        ,self.mmtTime  ,0.5*(self.mmtTime**2) ,0        ,0             ,0                    ],
         [0        ,1             ,self.mmtTime          ,0        ,0             ,0                    ],
         [0        ,0             ,1                     ,0        ,0             ,0                    ],
         [0        ,0             ,0                     ,1        ,self.mmtTime  ,0.5*(self.mmtTime**2)],
         [0        ,0             ,0                     ,0        ,1             ,self.mmtTime         ],
         [0        ,0             ,0                     ,0        ,0             ,1                    ]]
        )
        self.Q = np.array(
        [[0.25*(self.mmtTime**4) ,0.5*(self.mmtTime**3) ,0.5*(self.mmtTime**2) ,0                      ,0                     ,0                    ],
         [0.5*(self.mmtTime**3)  ,self.mmtTime**2       ,self.mmtTime          ,0                      ,0                     ,0                    ],
         [0.5*(self.mmtTime**2)  ,self.mmtTime          ,1                     ,0                      ,0                     ,0                    ],
         [0                      ,0                     ,0                     ,0.25*(self.mmtTime**4) ,0.5*(self.mmtTime**3) ,0.5*(self.mmtTime**2)],
         [0                      ,0                     ,0                     ,0.5*(self.mmtTime**3)  ,self.mmtTime**2       ,self.mmtTime         ],
         [0                      ,0                     ,0                     ,0.5*(self.mmtTime**2)  ,self.mmtTime          ,1                    ]]
        )
        self.Q =  self.Q * (self.accDev ** 2)

        self.R = np.array(
        [[self.mmtErrDev**2 ,0           ],
         [0                 ,self.mmtErrDev**2]] 
        )

        self.P = np.array(
        [[500      ,0        ,0        ,0        ,0        ,0],
         [0        ,500      ,0        ,0        ,0        ,0],
         [0        ,0        ,500      ,0        ,0        ,0],
         [0        ,0        ,0        ,500      ,0        ,0],
         [0        ,0        ,0        ,0        ,500      ,0],
         [0        ,0        ,0        ,0        ,0        ,500]]
        )

        #Initial Predict
        self.P = np.matmul(self.F,self.P)
        self.P = np.matmul(self.P,self.F.transpose())

        self.Kgain =  np.array([])

        self.i = 0 
        self.zi = np.array(
        [[self.xSensorVals[self.i]],
         [self.ySensorVals[self.i]]] 
        )
    
    def filterData(self):
        while(self.i < self.xSensorVals.size):                           #xSensorVals.size
            #Kalman Gain equation
            self.zi = np.array([[self.xSensorVals[self.i]],
                                [self.ySensorVals[self.i]]])

            self.Kgain = np.matmul(np.matmul(self.P,self.H.transpose()),np.linalg.inv(np.matmul(np.matmul(self.H,self.P),self.H.transpose()) + self.R))

            XNN = np.matmul(self.Kgain,np.subtract(self.zi,np.matmul(self.H,self.Xn)))
            self.Xn = self.Xn + XNN
            if(self.xFilterVals.size <= self.mmtNum):
                self.xFilterVals = np.append(self.xFilterVals,self.Xn[0])
            if(self.yFilterVals.size <= self.mmtNum):
                self.yFilterVals = np.append(self.yFilterVals,self.Xn[3])

            self.I = np.identity(6)
            self.P = np.matmul(np.matmul((self.I - np.matmul(self.Kgain,self.H)),self.P),(self.I - np.matmul(self.Kgain,self.H)).transpose()) + np.matmul(np.matmul(self.Kgain,self.R),self.Kgain.transpose())

            self.Xn = np.matmul(self.F,self.Xn)

            self.P = np.matmul(np.matmul(self.F,self.P),self.F.transpose()) + self.Q
    
            self.i += 1

    def printData(self):
        print(self.xFilterVals)    
        print(self.yFilterVals) 

    def getFilterDev(self):
        sumdev = 0
        i = 0
        while(i < self.mmtNum):
            sumdev = sumdev + ((self.xFilterVals[i] - self.dat.getxTrueVals()[i])**2 + (self.yFilterVals[i] - self.dat.getyTrueVals()[i])**2)
            i = i+1
        avdev = sumdev/self.mmtNum
        stddev = (avdev)**0.5
        return stddev
    
    def plotData(self):
        plt.xlim(-450, 350)
        plt.ylim(-50, 350)
        plt.gca().set_aspect('equal', adjustable='box')

        plt.plot(self.dat.getxTrueVals(), self.dat.getyTrueVals(), marker="o", markersize=3, markerfacecolor="green")
        plt.plot(self.dat.getxSensorVals(), self.dat.getySensorVals(), marker="o", markersize=2, markerfacecolor="red")
        plt.plot(self.xFilterVals, self.yFilterVals, marker="o", markersize=1, markerfacecolor="blue")

        plt.grid()
        plt.show()

Kf = KalmanFilter(dataset1)
Kf.filterData()
Kf.plotData()

print("sensor dev : ",dataset1.getSensorDev())
print("filter dev : ",Kf.getFilterDev())