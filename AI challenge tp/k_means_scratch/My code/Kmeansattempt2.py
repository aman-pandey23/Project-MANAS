import random
import math
import sys

class KMeans:
    def __init__(
      self, n_clusters=20, init='mn_2sg_rng', n_init=10, max_iter=1000):
        self.n_clusters = n_clusters
        self.init = init
        self.n_init = n_init
        self.max_iter = max_iter
        self.clr_arr = ['blue', 'red', 'yellow', 'green', 'cyan', 'magenta']
    def __get_mins_and_maxs__(self, KNN_A):
        number_of_points = len(KNN_A)
        number_of_dimensions = len(KNN_A[0])

        mins = [1e10] * number_of_dimensions
        maxs = [-1e10] * number_of_dimensions

        for i in range(number_of_points):
            for j in range(number_of_dimensions):
                if KNN_A[i][j] < mins[j]:
                    mins[j] = KNN_A[i][j]
                if KNN_A[i][j] > maxs[j]:
                    maxs[j] = KNN_A[i][j]

        return mins, maxs

    def __get_random_point_from_point__(self, arr, half_range):
        number_of_dimensions = len(arr)

        pt = []
        for i in range(number_of_dimensions):
            var = random.uniform(-half_range[i], half_range[i])
            pt.append(arr[i]+var)

        return pt

    def __get_random_point_in_range__(self, mins, maxs):
        pt = []
        for i in range(len(mins)):
            pt.append(random.uniform(mins[i], maxs[i]))

        return pt

    def __get_distribution_parameters_of_pts__(self, KNN_A):
        num_pts = len(KNN_A)
        number_of_dimensions = len(KNN_A[0])

        means = [0] * number_of_dimensions
        stds = [0] * number_of_dimensions
        for arr in KNN_A:
            for i in range(number_of_dimensions):
                means[i] += arr[i]
        for i in range(number_of_dimensions):
            means[i] /= num_pts
        for arr in KNN_A:
            for i in range(number_of_dimensions):
                stds[i] += (means[i] - arr[i])**2
        for i in range(number_of_dimensions):
            stds[i] = (stds[i] / num_pts)**0.5

        return means, stds

    def __get_distance_between_two_points__(self, arr1, arr2):
        sq_dist = 0
        for i in range(len(arr1)):
            sq_dist += (arr1[i] - arr2[i])**2

        return sq_dist**0.5

    def __group_points_by_centroids__(self, grps, KNN_C, KNN_A):
        for pta in KNN_A:
            minD = 1e10
            for i in range(len(KNN_C)):
                ptc = KNN_C[i]
                dist = self.__get_distance_between_two_points__(
                    ptc, pta)
                if dist < minD:
                    closest_centroid = i
                    minD = dist

            grps[closest_centroid]['points'].append(pta)
            if grps[closest_centroid]['centroids'] == []:
                grps[closest_centroid]['centroids'] = \
                    KNN_C[closest_centroid]

        return grps

    def __determine_inertia__(self, grps):
        inertia = 0
        for i in range(len(grps)):
            for j in range(len(grps[i]['points'])):
                dist = self.__get_distance_between_two_points__(
                        grps[i]['centroids'],
                        grps[i]['points'][j])
                inertia += (dist) ** 2

        return inertia

    def __update_centroids__(self, grps, KNN_A):

        KNN_C_New = []
        total_number_of_clusters = len(grps)
        number_of_dimensions = len(KNN_A[0])
        mins, maxs = self.__get_mins_and_maxs__(KNN_A)

        for i in range(total_number_of_clusters):
            number_of_points_in_cluster = len(grps[i]['points'])
            if number_of_points_in_cluster == 0:
                KNN_C_New.append(
                    self.__get_random_point_in_range__(mins, maxs))
                grps[i]['centroids'] = KNN_C_New[-1]
                continue 

            cnt_locs = [0] * number_of_dimensions

            for j in range(number_of_dimensions):
                for k in range(number_of_points_in_cluster):
                    cnt_locs[j] += grps[i]['points'][k][j]
                cnt_locs[j] /= number_of_points_in_cluster
            grps[i]['centroids'] = cnt_locs
            KNN_C_New.append(cnt_locs)

        return KNN_C_New, grps

    def __find_Arrays_delta__(self, KNN_C, KNN_C_New):
        dist_sum = 0
        for i in range(len(KNN_C)):
            dist_sum += self.__get_distance_between_two_points__(
                KNN_C[i], KNN_C_New[i])

        return dist_sum

    def __initial_disbursement_of_centroids__(
      self, KNN_A, n_clusters, method='mn_2sg_rng'):
        means, stds = self.__get_distribution_parameters_of_pts__(
            KNN_A)
        two_sig = []
        for element in stds:
            two_sig.append(element*2.0)
        KNN_C = []

        if method == 'mn_2sg_rng':
            for i in range(n_clusters):
                KNN_C.append(
                    self.__get_random_point_from_point__(
                        means, two_sig))

            return KNN_C

    def determine_k_clusters(self, KNN_A):
        min_inertia = 1e10
        for attempt in range(self.n_init):
            KNN_C = self.__initial_disbursement_of_centroids__(
                KNN_A, self.n_clusters)

            # Loop beginning
            cnt = 0
            while cnt < self.max_iter:
                grps = {}
                for i in range(self.n_clusters):
                    grps[i] = {'centroids': [], 'points': []}

                # Find groups by closest to centroid
                grps = self.__group_points_by_centroids__(grps, KNN_C, KNN_A)

                KNN_C_New, grps = self.__update_centroids__(grps, KNN_A)

                delta_As = self.__find_Arrays_delta__(KNN_C, KNN_C_New)

                if delta_As == 0:
                    break

                KNN_C = KNN_C_New

                cnt += 1

            #######
            current_inertia = self.__determine_inertia__(grps)
            if current_inertia < min_inertia:
                min_inertia = current_inertia
                grps_best = grps

        self.inertia_ = min_inertia
        return grps_best


###############################################################################

#Get data
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
KNN_A = Data
###############################################################################

kmeans = KMeans(n_clusters=clusters)
grps = kmeans.determine_k_clusters(KNN_A)

'''
kmeans.plot_clusters(grps)
'''

cent= []

for i in range(0,clusters):
    centroid_x = grps[i]['centroids'][0]
    centroid_y = grps[i]['centroids'][1]
    x_val = int(centroid_x)
    y_val = int(centroid_y)
    cent.append([x_val,y_val])

sorted_cent = sorted(cent, key=lambda x:(x[0], x[1]))

for i in sorted_cent:
    print(float(i[0]),float(i[1]))