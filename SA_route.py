import numpy as np
import pandas as pd
import math
from random import *
from cluster import *
from swap import *

class SA():
    def __init__(self):
        pass

    def Route(self, route_array, index_list):
        array_length = len(route_array)
        distance_matrix = np.zeros((array_length, array_length))
        # '''
        # Create an empty matrix to store distance from points to point
        # '''

        # print(index_list)

        for i in range(array_length):
            for j in range(array_length):
                distance_matrix[i, j] = math.sqrt((route_array[i][0] - route_array[j][0])**2 \
                                  + (route_array[i][1] - route_array[j][1])**2 )

        distance_matrix = distance_matrix + distance_matrix.T

        index_dict = dict(enumerate(index_list))

        pickup_index0 = [ind[0] for ind in enumerate(index_list)]

        pickup_index = pickup_index0[1: len(pickup_index0)-1]

        copy_pickup_index = pickup_index

        # pickup_index = index_list[1: len(index_list)-1]
        # print(pickup_index)
        # copy_pickup_index = pickup_index

        shuffle(pickup_index)

        # '''
        # Create pickup index, and shuffle them randomly.
        # Note that start point and end point are excluded.
        # Only shuffle the pickup points.
        # '''

        start_index = pickup_index0[0]

        end_index = pickup_index0[-1]

        # path = [0] + pickup_index + [array_length-1]
        path = [start_index] + list(pickup_index) + [end_index]
        # print(path)

        # '''
        # Initilize a path.
        # The path includes start and end points.
        # '''

        trip_distance = 0 # Initial total distance of trips
        for i in range(0,array_length-1):
            trip_distance = trip_distance + distance_matrix[path[i]][path[i+1]]

        # '''
        # The minimum value of trip_distance is the objective we need to find out.
        # '''

        # Initial SA parameters

        T_end = 0
        L = 2000
        delta_T = 0.99
        T = 1

        for _ in range(L):
            shuffle(copy_pickup_index)

            swap = copy_pickup_index[:2]
            swap = sorted(swap)
            c1 = swap[0]
            c2 = swap[1]

            new_distance = distance_matrix[path[c1-1]][path[c2]] + distance_matrix[path[c1]][path[c2+1]] \
                           - distance_matrix[path[c1-1]][path[c1]] - distance_matrix[path[c2]][path[c2+1]]

            if new_distance < 0:
                path = path[0:c1] + path[c2:c1 - 1:-1] + path[c2 + 1:array_length]
                trip_distance = trip_distance + new_distance

            elif math.exp(-new_distance / T) > random():
                path = path[0:c1] + path[c2:c1 - 1:-1] + path[c2 + 1:array_length]
                trip_distance = trip_distance + new_distance

            T = T * delta_T
            if T < T_end:
                break

        path_res = [index_dict[p] for p in path]

        return path_res, trip_distance


    def Car(self, centroid_df, car_df):
        '''

        :param centroid_df: Should contain centroids' location and label
        :param car_df: Should contain cars' location and unique id
        :return: 从第一辆车开始，派到区域的顺序。例，返回[2,0,1], 第一辆车接第三区，第二辆车接1区，第三辆接2区。
        '''

        car_length = car_df.shape[0]
        distance_matrix = np.zeros((car_length, car_length))   #创建空向量， 来存储点与点之间的距离

        enum_pickup_index = list(enumerate(centroid_df['label'].tolist()))
        centroid_label_dict = dict(enum_pickup_index)
        #由于每次得到的label不一样， 需要给创建一个dict来保存index。接下来就是用生成的序号进行运算，最后再找回原来的。
        print(centroid_label_dict)

        pickup_index = [ind[0] for ind in enum_pickup_index]
        path = [ind[0] for ind in enum_pickup_index]
        copy_pickup_index = [ind[0] for ind in enum_pickup_index]
        # plan_path = [ind[0] for ind in enum_pickup_index]

        for i in range(car_length):
            for j in pickup_index:
                distance_matrix[i,j] = math.sqrt((car_df['lat'][i] - centroid_df['lat'][j])**2 \
                                                  + (car_df['lng'][i] - centroid_df['lng'][j])**2)

        print(distance_matrix)

        trip_distance = 0
        for i in range(0, car_length):
            trip_distance = trip_distance + distance_matrix[i][path[i]]  # 先根据path得出一个初始的总距离值


        #初始化SA参数
        T_end = 0
        L = 2000
        delta_T = 0.99
        T = 1

        for _ in range(L):

            shuffle(copy_pickup_index)
            swap = copy_pickup_index[:2]
            swap = sorted(swap)

            c1 = swap[0]
            c2 = swap[1]

            plan_path = Swap2(path)
            plan_path.swap(c1,c2)          #交换index为c1， c2位置的值， 得到新的组合

            new_distance = 0
            for j in range(0,car_length):
                new_distance = new_distance + distance_matrix[j][plan_path[j]]

            delta_distance = new_distance - trip_distance

            if delta_distance < 0:         # 效果好，直接采用该path， 并更新总路程。
                # print("better result, accept")
                trip_distance = new_distance
                path = plan_path

            elif math.exp(-delta_distance / T) > random():  #效果不好，但是通过了接受概率，就可以接受该结果。
                # print("bad result, accept")
                trip_distance = new_distance
                path = plan_path

            # Update T until reach threshold
            T = T * delta_T
            if T < T_end:
                break


        new_path = [centroid_label_dict[p] for p in path]  #还原成原本的index

        return new_path






