import numpy as np
import pandas as pd
import math
from random import *
from cluster import Cluster
from swap import *
from SA_route import *
from Merge_route import *

class Optimize():

    def __init__(self, pickup_point_df, car_df, destination_df, k):
        '''

        :param pickup_point_df: Dataframe. column name: lat, lng, index
        :param car_df: Dataframe. column name: lat, lng, index
        :param destination_df: Dataframe. column name: lat, lng, index or id or any unique value
        :param k: k cluster for K means
        '''
        # self.pickup_point_df = pickup_point_df
        self.car_df = car_df
        self.car_df['index'] = -self.car_df['index'] # Change car index, in case it is the same to pickup index.
        self.car_x, self.car_y = self.car_df['lat'].values, self.car_df['lng'].values
        self.car_points = np.array([[i, j] for i,j in zip(self.car_x, self.car_y)])
        self.car_index = self.car_df['index'].values

        self.destination_df = destination_df
        self.end_x, self.end_y = self.destination_df['lat'].values, self.destination_df['lng'].values
        self.end_point = np.array([[i, j] for i,j in zip(self.end_x, self.end_y)])
        self.end_index = self.destination_df['index'].values

        self.k = k

        self.x, self.y = pickup_point_df['lat'].values, pickup_point_df['lng'].values
        self.pickup_points = np.array([[i, j] for i,j in zip(self.x, self.y)])
        self.index_pickup = pickup_point_df['index'].tolist()

        self.cluster = Cluster(k=self.k, route_array=self.pickup_points, index_list=self.index_pickup)
        self.sa = SA()

    def _cluster_info(self):
        centroid_df = pd.DataFrame.from_records(self.cluster.centroid, columns=['lat', 'lng'])
        centroid_df['label'] = self.cluster.predict(self.cluster.centroid)

        label_points_index = self.cluster.point_in_cluster

        return centroid_df, label_points_index

    @property
    def run(self):

        centroid_df, label_points_index = self._cluster_info()
        print(centroid_df)
        print(self.car_df)
        cluster_order = self.sa.Car(centroid_df, self.car_df)   # get 1st car to which cluster, 2nd to which one, and so on
        print(cluster_order)
        result = {}

        for i in range(self.k):

            routes = Merge.merge_start_end_route(np.array([self.car_points[i]]), label_points_index[str(cluster_order[i])]['route_point'], np.array([self.end_point[0]]))
            route_index = Merge.merge_start_end_index(np.array([self.car_index[i]]), label_points_index[str(cluster_order[i])]['route_index'], np.array([self.end_index[0]]))

            path, distance = self.sa.Route(routes, route_index)

            result['Route' + str(i)] = {'Path': path, 'Distance': distance, 'Cluster': cluster_order[i]}

        return result


if __name__ == '__main__':
    pickup_points_df = pd.read_csv("sim_route.csv")
    car_df = pd.read_csv("sim_cars.csv")
    destination_df = pd.read_csv("sim_end.csv")

    k = 3
    test = Optimize(pickup_point_df=pickup_points_df, car_df=car_df, destination_df=destination_df, k=k).run
    print(test)

