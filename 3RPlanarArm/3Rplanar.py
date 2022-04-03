import math
import matplotlib
matplotlib.__version__
import matplotlib.pyplot as plt

theta1 = 0
theta2 = 0
theta1 = 0

xw = 0
yw = 0

xe = 0
ye = 0

l1 = 0
l2 = 0
l3 = 0

def cosCalc(a, b, c):
        angle = math.acos((a*a + b*b - c*c)/(2*a*b))
        return angle
    
def getThetas():
        global theta1
        global theta2
        global theta3
        global xw
        global yw
        global xe
        global ye
        global l1
        global l2
        global l3
        xe = float(input("xe: "))
        ye = float(input("ye: "))
        phie = math.radians(float(input("phie in degrees: ")))
        l1 = float(input("l1: "))
        l2 = float(input("l2: "))
        l3 = float(input("l3: "))
        
        xw = xe - l3 * math.cos(phie)
        yw = ye - l3 * math.sin(phie)
        r = math.sqrt(xw**2 + yw**2)
        gamma = cosCalc(r, l1, l2)
        
        theta2 = math.pi - cosCalc(l1, l2, r)
        theta1 = math.atan2(yw, xw) - gamma
        theta3 = phie - theta1 - theta2
        
        print("theta1: ",math.degrees(theta1)," and ", math.degrees(theta1 + 2 * gamma))
        print("theta2: ",math.degrees(theta2)," and ", math.degrees(theta2 * - 1))
        print("theta3: ",math.degrees(theta3)," and ", math.degrees(theta3 + 2 * (theta2 - gamma)))


getThetas()

Ax = l1*math.cos(theta1)
Ay = l1*math.sin(theta1)

Bx = Ax + l2*math.cos(theta1+theta2) 
By = Ay + l2*math.sin(theta1+theta2) 

Cx = Bx + l3*math.cos(theta1+theta2+theta3)
Cy = By + l3*math.sin(theta1+theta2+theta3)

x1,y1 = [0],[0]
x2,y2 = [Ax],[Ay]
x3,y3 = [Bx],[By]
x4,y4 = [Cx],[Cy]

plt.axis('scaled')
plt.plot(x1, y1, marker="o", markersize=10, markerfacecolor="green")
plt.plot(x2, y2, marker="o", markersize=10, markerfacecolor="red")
plt.plot(x3, y3, marker="o", markersize=10, markerfacecolor="yellow")
plt.plot(x4, y4, marker="o", markersize=10, markerfacecolor="blue")

x1, y1 = [0, Ax], [0, Ay]
x2, y2 = [Ax, Bx], [Ay, By]
x3, y3 = [Bx, Cx], [By, Cy]
plt.axis('square')
plt.plot(x1, y1, marker = 'o',color = "green",linewidth = 30)
plt.plot(x2, y2, marker = 'o',color = "red",linewidth = 20)
plt.plot(x3, y3, marker = '8', color = "blue",linewidth = 15)

plt.show()
