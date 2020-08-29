#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
# Copyright 2015 Tin Arm Engineering AB
# Copyright 2018 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Capacitated Vehicle Routing Problem with Time Windows (CVRPTW).
   This is a sample using the routing library python wrapper to solve a CVRPTW
   problem.
   A description of the problem can be found here:
   http://en.wikipedia.org/wiki/Vehicle_routing_problem.
   Distances are in meters and time in minutes.
"""

from __future__ import print_function

from functools import partial
from six.moves import xrange

from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
from scipy.spatial import distance_matrix

import pandas as pd
df=pd.read_excel(r'/Users/MuditPaliwal/Desktop/Data.xlsx')

print(df)

x = df.iloc[:,1]
y = df.iloc[:,2]
d = df.iloc[:,3]
data =  [(f,b) for(f,b) in zip(x,y)]
ctys = range(51)
df = pd.DataFrame(data, columns=['xcord', 'ycord'], index=ctys)
dist = pd.DataFrame(distance_matrix(df.values, df.values), index=df.index, columns=df.index)


###########################
# Problem Data Definition #
###########################
def create_data_model():
    """Stores the data for the problem"""
    data = {}
    # Locations in block unit
    _locations = [(0.0, 0.0), (-8.2, -96.68), (-16.01, 14.95), (-1.26, 82.05), (-93.17, 78.92), (-57.1, 18.67), (89.57, 13.12), (-99.8, 27.28), (0.79, -33.16), (78.95, 78.61), (80.92, -39.92), (-95.76, 79.96), (-31.53, 54.57), (-18.47, -31.8), (-96.29, -53.0), (85.06, -45.54), (37.84, 75.75), (-2.38, -40.04), (-37.7, 25.98), (-74.47, 74.73), (85.66, 88.39), (-97.99, 67.34), (-66.24, 47.94), (49.66, -9.73), (66.59, -84.24), (9.82, 22.22), (38.45, -6.1), (-24.67, -77.81), (5.55, 88.13), (85.59, 14.86), (89.28, 89.99), (-47.88, 76.3), (19.9, -47.07), (11.24, 62.22), (16.26, 88.32), (79.24, -44.43), (-99.97, 27.93), (1.01, -60.47), (-51.98, -42.88), (8.71, -23.44), (-82.64, 87.2), (30.8, -8.29), (6.28, 44.43), (25.02, 78.73), (31.69, 62.16), (-36.28, -25.46), (45.35, 77.33), (67.7, -89.31), (-2.42, 71.68), (10.45, 66.92), (-21.02, 30.19)]
    # Compute locations in meters using the block dimension defined as follow
    # Manhattan average block: 750ft x 264ft -> 228m x 80m
    # here we use: 114m x 80m city block
    # src: https://nyti.ms/2GDoRIe "NY Times: Know Your distance"
    data['locations'] = [(l[0] * 114, l[1] * 80) for l in _locations]
    data['num_locations'] = len(data['locations'])
    data['time_windows'] =[(0, 5), (222, 234), (1378, 1433), (1115, 1136), (1289, 1312), (656, 698), (221, 253), (1086, 1105), (560, 627), (1084, 1143), (1168, 1187), (337, 340), (756, 809), (1316, 1328), (124, 189), (1286, 1313), (154, 221), (21, 78), (834, 853), (735, 816), (386, 425), (1277, 1341), (1202, 1262), (1269, 1336), (1238, 1251), (1045, 1057), (99, 153), (380, 400), (569, 644), (933, 985), (401, 429), (1027, 1073), (959, 1019), (558, 626), (1245, 1269), (603, 642), (1088, 1144),    (127, 172), (764, 785), (473, 517), (875, 890), (597, 641), (460, 484), (23, 97), (403, 463), (299, 348), (1018, 1093), (1078, 1120), (1369, 1396), (487, 503), (1133, 1170)]
    data['demands'] = d
    data['time_per_demand_unit'] = 0.16666667  # 5 minutes/unit
    data['num_vehicles'] = 20
    data['vehicle_capacity'] = 80
    data['vehicle_speed'] = 1666.67  # Travel speed: 5km/h converted in m/min
    data['depot'] = 0
    return data


#######################
# Problem Constraints #
#######################
def euclidean_distance(position_1, position_2):
    """Computes the Manhattan distance between two points"""
    return (
        abs(position_1[0] - position_2[0]) + abs(position_1[1] - position_2[1]))


def create_distance_evaluator(data):
    """Creates callback to return distance between points."""
    _distances = {}
    # precompute distance between location to have distance callback in O(1)
    for from_node in xrange(data['num_locations']):
        _distances[from_node] = {}
        for to_node in xrange(data['num_locations']):
            if from_node == to_node:
                _distances[from_node][to_node] = 0
            else:
                _distances[from_node][to_node] = (euclidean_distance(
                    data['locations'][from_node], data['locations'][to_node]))

    def distance_evaluator(manager, from_node, to_node):
        """Returns the manhattan distance between the two nodes"""
        return _distances[manager.IndexToNode(from_node)][manager.IndexToNode(
            to_node)]

    return distance_evaluator
    print (distance_evaluator)

data['demands'][node] * data['time_per_demand_unit']
