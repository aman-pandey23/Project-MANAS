import numpy as np
import random
import time
import math
import matplotlib.pyplot as plt

class CoordDataSet:
    xVals = np.array([])
    yVals = np.array([])

    xTrueVals = np.array([])
    yTrueVals = np.array([])
    xSensorVals = np.array([])
    ySensorVals = np.array([])

    
    # Dataset Variables
    mmtTime = 1
    accDev = 0.2
    mmtErrDev = 3
    mmtNum = 35

    # Motion Path Setting Variables
    initX = -400
    initY = 300
    curX=initX
    curY=initY
    vel = 26

    turn_radius = 300
    thetaI = 1.57
    thetaF = -1.57
    curTheta = thetaI
    delTheta = thetaI - thetaF
    omega = vel/turn_radius
    dTheta = omega * mmtTime

    def __init__(self, mtime, stdDev, mnum):
        self.mmtTime = mtime
        self.mmtErrDev = stdDev
        self.mmtNum = mnum
    
    def getCoords(self, tm):
        if(self.curX >= 0):
            if(self.curTheta >= self.thetaF):
                self.curTheta -= self.dTheta
                self.curX = self.turn_radius*math.cos(self.curTheta)
                self.curY = self.turn_radius*math.sin(self.curTheta)
                self.xTrueVals = np.append(self.xTrueVals, round((self.turn_radius*math.cos(self.curTheta)),3))
                self.yTrueVals = np.append(self.yTrueVals, round((self.turn_radius*math.sin(self.curTheta)),3))
        if(self.curX <= 0): 
            self.curX = self.initX + self.vel*tm 
            self.curY = self.initY
            self.xTrueVals = np.append(self.xTrueVals, round((self.initX + self.vel*tm),3))
            self.yTrueVals = np.append(self.yTrueVals, round(self.initY,3))
    
    def generateData(self):
        itm = 0
        tmEnd = self.mmtNum * self.mmtTime
        while(itm < tmEnd):
            self.getCoords(itm)
            itm += self.mmtTime
        xnoise = np.random.normal(0, self.mmtErrDev, self.xTrueVals.shape)
        ynoise = np.random.normal(0, self.mmtErrDev, self.yTrueVals.shape)
        self.xSensorVals = self.xTrueVals + xnoise
        self.ySensorVals = self.yTrueVals + xnoise
    
    def getMmt(self):
        return self.mmtTime
    
    def getmmtNum(self):
        return self.mmtNum
    
    def getxTrueVals(self):
        return self.xTrueVals
    
    def getyTrueVals(self):
        return self.yTrueVals

    def getxSensorVals(self):
        return self.xSensorVals
    
    def getySensorVals(self):
        return self.ySensorVals
    
    def getaccDev(self):
        return self.accDev

    def getstdDev(self):
        return self.mmtErrDev

    def showRealVals(self):
        print("real x :")
        print(self.xTrueVals)
        print("real y :")
        print(self.yTrueVals)
        print("__________")
    
    def showSensorVals(self):
        print("Sensor x :")
        print(self.xSensorVals)
        print("Sensor y :")
        print(self.ySensorVals)
        print("__________")

    def getSensorDev(self):
        sumdev = 0
        i = 0
        while(i < self.mmtNum):
            sumdev = sumdev + ((self.xSensorVals[i] - self.xTrueVals[i])**2 + (self.ySensorVals[i] - self.yTrueVals[i])**2)
            i = i+1
        avdev = sumdev/self.mmtNum
        stddev = (avdev)**0.5
        return stddev
    
    def plotData(self):
        plt.xlim(-450, 350)
        plt.ylim(-50, 350)
        plt.gca().set_aspect('equal', adjustable='box')

        plt.plot(self.xTrueVals, self.yTrueVals, marker="o", markersize=3, markerfacecolor="green")
        plt.plot(self.xSensorVals, self.ySensorVals, marker="o", markersize=2, markerfacecolor="red")

        plt.grid()
        plt.show()

