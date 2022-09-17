import numpy as np
import random
import time
import math
import matplotlib.pyplot as plt
import GenerateDataSet as gen

dataset1 = gen.CoordDataSet(1,3,50)
dataset1.generateData()

class KalmanFilter:

    xFilterVals = np.array([])
    yFilterVals = np.array([])
    
    """
    The measurements period: Δt=1s
    The random acceleration standard deviation: σa=0.2ms2
    The measurement error standard deviation: σxm=σym=3m
    """


    #NEEDED CONSTANTS
    mmtTime = 0.1
    accDev = 0.2
    mmtErrDev = 0.3
    
    #iteration count
    i = 0

    def __init__(self):
        
        self.H = np.array(
            [[1,0,0,0,0,0],    
             [0,0,0,1,0,0]]
        )
        #initial state matrix
        self.Xn = np.array(
            [[0],
             [0],
             [0],
             [0],
             [0],
             [0]]
        )
        #state transition matrix F
        self.F = np.array(
        [[1        ,self.mmtTime  ,0.5*(self.mmtTime**2) ,0        ,0             ,0                    ],
         [0        ,1             ,self.mmtTime          ,0        ,0             ,0                    ],
         [0        ,0             ,1                     ,0        ,0             ,0                    ],
         [0        ,0             ,0                     ,1        ,self.mmtTime  ,0.5*(self.mmtTime**2)],
         [0        ,0             ,0                     ,0        ,1             ,self.mmtTime         ],
         [0        ,0             ,0                     ,0        ,0             ,1                    ]]
        )
        #process noise matrix Q 
        self.Q = np.array(
        [[0.25*(self.mmtTime**4) ,0.5*(self.mmtTime**3) ,0.5*(self.mmtTime**2) ,0                      ,0                     ,0                    ],
         [0.5*(self.mmtTime**3)  ,self.mmtTime**2       ,self.mmtTime          ,0                      ,0                     ,0                    ],
         [0.5*(self.mmtTime**2)  ,self.mmtTime          ,1                     ,0                      ,0                     ,0                    ],
         [0                      ,0                     ,0                     ,0.25*(self.mmtTime**4) ,0.5*(self.mmtTime**3) ,0.5*(self.mmtTime**2)],
         [0                      ,0                     ,0                     ,0.5*(self.mmtTime**3)  ,self.mmtTime**2       ,self.mmtTime         ],
         [0                      ,0                     ,0                     ,0.5*(self.mmtTime**2)  ,self.mmtTime          ,1                    ]]
        )
        self.Q =  self.Q * (self.accDev ** 2)

        #measurement uncertainty R
        self.R = np.array(
        [[self.mmtErrDev**2 ,0           ],
         [0                 ,self.mmtErrDev**2]] 
        )
        
        #initial state vector with very high estimate uncertainty. more value to measurement
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

        #
        self.i = 0 

    def getFilteredData(self,coord):

        self.zi = np.array([coord[0],coord[1]])

        self.Kgain = np.matmul(np.matmul(self.P,self.H.transpose()),np.linalg.inv(np.matmul(np.matmul(self.H,self.P),self.H.transpose()) + self.R))
        
        XNN = np.matmul(self.Kgain,np.subtract(self.zi,np.matmul(self.H,self.Xn)))
        
        self.Xn = self.Xn + XNN
        
        self.xFilterVals = np.append(self.xFilterVals,self.Xn[0])
        
        self.yFilterVals = np.append(self.yFilterVals,self.Xn[3])
        
        self.I = np.identity(6)
        
        self.P = np.matmul(np.matmul((self.I - np.matmul(self.Kgain,self.H)),self.P),(self.I - np.matmul(self.Kgain,self.H)).transpose()) + np.matmul(np.matmul(self.Kgain,self.R),self.Kgain.transpose())
        
        self.Xn = np.matmul(self.F,self.Xn)
        
        self.P = np.matmul(np.matmul(self.F,self.P),self.F.transpose()) + self.Q

        
        
        self.i += 1
        out = np.array([[self.Xn[0]],self.Xn[3]])
        return(out)



    def printData(self):
        print(self.xFilterVals)    
        print(self.yFilterVals) 

    """
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
        plt.plot(self.xFilterVals, self.yFilterVals, marke< r="o", markersize=1, markerfacecolor="blue")

        plt.grid()
        plt.show()
    """
xSensorVals = dataset1.getxSensorVals()
ySensorVals = dataset1.getySensorVals()  
a = 0

xaFilterVals = np.array([])
yaFilterVals = np.array([])

Kf = KalmanFilter()

while a < xSensorVals.size:
    cordd = np.array([[xSensorVals[a]],[ySensorVals[a]]])
    cord = Kf.getFilteredData(cordd)
    xaFilterVals = np.append(xaFilterVals,cord[0])
    yaFilterVals = np.append(yaFilterVals,cord[1])
    
    plt.plot(xSensorVals, ySensorVals, marker="o", markersize=3, markerfacecolor="green")
    plt.plot(xaFilterVals, yaFilterVals, marker="o", markersize=3, markerfacecolor="red")
    print(cord)
    a = a+1

plt.show()