import random
import time
import math
import matplotlib.pyplot as plt
import numpy as np

xRange = 30
rsln = 0.1
dx = rsln
setPoint = 3

global prevErr
global prevIntg
prevErr = 0
prevIntg = 0

def proportional(err):
    kp = 1
    a = kp * err
    return a

def integral(err):
    global prevIntg
    ki = 0.2
    a = (prevIntg + err) * ki
    prevIntg = a
    return a

def derivative(err):
    kd = 2
    a = ((err - prevErr)/dx) * kd
    return a


def PID(err):
  pr = proportional(err)
  ing = integral(err)
  de = derivative(err)
  PIDv = pr + ing + de
  return PIDv

x = np.linspace(0,xRange,100)
y = setPoint + x*0
time = np.arange(0, xRange, 0.1)
amplitude = np.sin(time)
plt.plot(x, y)
plt.plot(time, amplitude)


i = 0
while(i < xRange):
    if(i != 0):
        fval = np.sin(i)
        error = setPoint - fval
        fdb = PID(error)
        prevErr = error
        x1,y1 = [i],[fdb]
        plt.plot(x1, y1, marker="o", markersize=1, markerfacecolor="green")
    i = i + rsln

plt.grid()
plt.show()
