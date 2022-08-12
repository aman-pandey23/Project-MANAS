class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
def Left_index(points):
    minn = 0
    for i in range(1,len(points)):
        if points[i].x < points[minn].x:
            minn = i
        elif points[i].x == points[minn].x:
            if points[i].y > points[minn].y:
                minn = i
    return minn

def orientation(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - \
          (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2

def convexHull(points, n):
     
    # There must be at least 3 points
    if n < 3:
        return
 
    # Find the leftmost point
    l = Left_index(points)
 
    hull = []
    p = l
    q = 0
    while(True):
         
        # Add current point to result
        hull.append(p)
        q = (p + 1) % n
 
        for i in range(n):
             
            # If i is more counterclockwise
            # than current q, then update q
            if(orientation(points[p],
                           points[i], points[q]) == 2):
                q = i
 
        p = q
 
        # While we don't come to first point
        if(p == l):
            break
 
    # Print Result
    out = []
    for each in hull:
        out.append([points[each].x, points[each].y])
    return out    
        
points = []
points.append(Point(0, 3))
points.append(Point(2, 2))
points.append(Point(1, 1))
points.append(Point(2, 1))
points.append(Point(3, 0))
points.append(Point(0, 0))
points.append(Point(3, 3))
a = convexHull(points, len(points))
print(a)