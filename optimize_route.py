import pandas as pd
import numpy as np
import math
from random import *
from cluster import *
from SA_route import *

class Optimize():
    def __init__(self,):
        pass

    @staticmethod
    def merge_start_end_route(start_loc, route, end_loc):

        route = np.append(start_loc, route, 0)
        route = np.append(route, end_loc, 0)

        return route

    @staticmethod
    def merge_start_end_index(start_index, route_index, end_index):

        route_index = np.append(start_index, route_index, 0)
        route_index = np.append(route_index, end_index, 0)

        return route_index


if __name__ == '__main__':
    pass
    # df = pd.read_csv("sim_route.csv")
    # x, y = df['lat'].values, df['lng'].values
    # routine = np.array([[i, j] for i, j in zip(x, y)])
    # # print(routine)
    # index_list = df['index'].tolist()
    #
    # centroid = 3
    # cluster = Cluster(k=centroid, route_array=routine, index_list=index_list)
    # # print(cluster.centroid)
    # # label_list = cluster.labels
    #
    # # route_point, route_index = cluster.point_in_cluster
    #
    # center_df = pd.DataFrame.from_records(cluster.centroid, columns=['lat', 'lng'])
    # center_df['label'] = cluster.predict(cluster.centroid)
    # # print(center_df)
    #
    # car_df = pd.read_csv("sim_cars.csv")
    # car_df['index'] = -car_df['index']
    # # print(car_df)
    #
    # sa = SA_route()
    # print(sa.SA_car(center_df, car_df))
