import random

def get_distance(point_1,point_2):
    return(((point_1[0]- point_2[0])**2 + (point_1[1]- point_2[1])**2)** 0.5)

def initialize_centroids(data,k):
    x_min = y_min = float('inf')
    x_max = y_max = float('-inf')
    for point in data: 
        x_min = min(point[0],x_min)
        x_max = max(point[0],x_max)
        y_min = min(point[0],y_min)
        y_max = max(point[0],y_max)
    centroids = []
    for i in range(k):
        centroids.append([random_sample(x_min,x_max),random_sample(y_min,y_max)])
    return centroids

def initialize_centroids_bad(x,k):
    return x[:k]

def update_centroids(points,labels,k):
    new_centroids = [[0,0] for i in range(k)]
    counts = [0] * k
    for point , label in zip(points,labels):
        new_centroids[label][0] += point[0]
        new_centroids[label][1] += point[1]
        counts[label] += 1
    
    for i, (x,y) in enumerate(new_centroids):
        new_centroids[i] = (x/counts[i],y/counts[i])
    return new_centroids

def should_stop(old_centroids,new_centroids,threshold = 1e-5):
    total_movement = 0
    for old_point,new_point in zip(old_centroids,new_centroids):
        total_movement += get_distance(old_point,new_point)
    return total_movement < threshold

def main(data,k):
    centroids = initialize_centroids(data,k)
    
    while True:
        old_centroids = centroids
        labels = get_labels(data, centroids)
        centroids = update_centroids(data,labels,k)
        
        if should_stop(old_centroids,centroids):
            break
    
    return labels

def random_sample(low,high):
    return low + (high-low) * random.random()


def get_labels(data,centroids):
    labels = []
    for point in data:
        min_dist = float('inf')
        label = None
        for i, centroid in enumerate(centroids):
            new_dist = get_distance(point,centroid)
            if min_dist > new_dist:
                min_dist = new_dist
                label = i
        labels.append(label)
    return labels

#########################

a = input()
b = a.split(" ")
rows = int(b[0])
columns = int(b[1])
clusters = int(b[2])
raw_data = []
i = 0
while (i < rows):
    line = input()
    if line:
        raw_data.append(line)
    else:
        break
    i = i+1
    
Data = []
i = rows-1
while (i >= 0):
    j = 0
    while(j < columns):
        if(raw_data[i][j] == "1"):
            Data.append([j,abs(i+1 - columns)])
        j = j + 1
    i = i - 1

#########################

a = main(Data,clusters)

k = clusters
cent = []
for i in range(k):
    sum_x = 0
    sum_y = 0
    count = 0
    for j in range(0,len(a)):
        if(a[j] == i):
            count = count+1
            sum_x = sum_x + Data[j][0]
            sum_y = sum_y + Data[j][1]
    if(count == 0):
        count = 1
    cent.append([sum_x/count,sum_y/count])

sorted_cent = sorted(cent, key=lambda x:(x[0], x[1]))

for i in sorted_cent:
    print(int(i[0]),int(i[1]))