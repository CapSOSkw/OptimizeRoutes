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



