import pandas as pd
import numpy as np
from sklearn.cluster import KMeans


class Cluster():
    def __init__(self, k, route_array, index_list):
        self.k = k
        self.route_array = route_array
        self.index_list = index_list

    def _kmeans_model(self):
        kmeans_model = KMeans(n_clusters=self.k, max_iter=500, precompute_distances=True,
                      n_jobs=-1, algorithm='auto').fit(self.route_array)

        return kmeans_model

    @property
    def labels(self):
        return self._kmeans_model().labels_

    @property
    def centroid(self):
        return self._kmeans_model().cluster_centers_

    @property
    def get_params(self):
        return self._kmeans_model().get_params()

    def predict(self, new_array):

        return self._kmeans_model().predict(new_array)

    @property
    def point_in_cluster(self):
        label_list = self.labels

        my_dict = {}
        for i in set(label_list):

            label_index = np.array([self.index_list[j] for j in np.where(label_list == i)[0]])
            # route_index.append(label_index)

            pickup_points = np.array([self.route_array[p] for p in label_index])
            # route_point.append(pickup_points)

            my_dict[str(i)] = {'route_point': pickup_points, 'route_index':label_index}
        # return route_point, route_index  # Modified on 01.28

        return my_dict
