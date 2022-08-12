import numpy as np
import random as rd
import math 

a = input()
b = a.split(" ")
rows = int(b[0])
columns = int(b[1])
clusters = int(b[2])
raw_data = []
i = 0
while (i < columns):
    line = input()
    if line:
        raw_data.append(line)
    else:
        break
    i = i+1
x = []
y = []
i = columns-1
while (i >= 0):
    j = 0
    while(j < rows):
        if(raw_data[i][j] == "1"):
            x.append(j+1)
            y.append(abs(i+1 - columns))
        j = j + 1
    i = i - 1


X_Y = list(zip(x, y))
X = np.asarray(X_Y)

m = len(x)
n = 2

n_iter = 100

K = clusters

Centroids =np.array([]).reshape(n,0) 

for i in range(K):
    rand=rd.randint(0,m-1)
    Centroids=np.c_[Centroids,X[rand]]
    
Output={}

EuclidianDistance=np.array([]).reshape(m,0)

for k in range(K):
    tempDist=np.sum((X-Centroids[:,k])**2,axis=1)
    EuclidianDistance=np.c_[EuclidianDistance,tempDist]
C=np.argmin(EuclidianDistance,axis=1)+1

Y={}
for k in range(K):
    Y[k+1]=np.array([]).reshape(2,0)
for i in range(m):
    Y[C[i]]=np.c_[Y[C[i]],X[i]]
     
for k in range(K):
    Y[k+1]=Y[k+1].T
    
for k in range(K):
     Centroids[:,k]=np.mean(Y[k+1],axis=0)
     
for i in range(n_iter):
     #step 2.a
      EuclidianDistance=np.array([]).reshape(m,0)
      for k in range(K):
          tempDist=np.sum((X-Centroids[:,k])**2,axis=1)
          EuclidianDistance=np.c_[EuclidianDistance,tempDist]
      C=np.argmin(EuclidianDistance,axis=1)+1
     #step 2.b
      Y={}
      for k in range(K):
          Y[k+1]=np.array([]).reshape(2,0)
      for i in range(m):
          Y[C[i]]=np.c_[Y[C[i]],X[i]]
     
      for k in range(K):
          Y[k+1]=Y[k+1].T
    
      for k in range(K):
          Centroids[:,k]=np.mean(Y[k+1],axis=0)
      Output=Y
      

'''
plt.scatter(X[:,0],X[:,1],c='black',label='unclustered data')
plt.legend()
plt.show()

color=['red','blue','green','cyan','magenta']
for k in range(K):
    plt.scatter(Output[k+1][:,0],Output[k+1][:,1],c=color[k])
plt.scatter(Centroids[0,:],Centroids[1,:],s=10,c='yellow',label='Centroids')
plt.legend()
plt.show()

print(Centroids)  

'''
cent = []

for i in range(K):
    key = i+1
    centroid_x = Centroids[0][i]
    centroid_y = Centroids[1][i]
    '''
    print("cent x = ",centroid_x)
    print("cent y = ",centroid_y)
    print("_______")
    '''
    x_val = 0
    y_val = 0
    min_dist = 200
    
    for j in range(0,len(Output[key])):
        '''
        print("X val : ",Output[key][j][0])
        print("Y val : ",Output[key][j][1])
        '''
        dist = math.sqrt((Output[key][j][0] - centroid_x)**2 + (Output[key][j][1] - centroid_y)**2)
        '''
        print("dist = ",dist)
        print("----")
        '''
        if(dist < min_dist):
            x_val = Output[key][j][0]
            y_val = Output[key][j][1]
            min_dist = dist
    cent.append([x_val,y_val])
    
'''
print(Centroids)    
print("_____")
print(cent)
'''

sorted_cent = sorted(cent, key=lambda x:(x[0], x[1]))

for i in sorted_cent:
    print(i[0]," ",i[1])