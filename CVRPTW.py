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
import math
from math import pow
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
    _locations = [(0,0), (-8.2, -96.68), (-16.01, 14.95), (-1.26, 82.05), (-93.17, 78.92), (-57.1, 18.67), (89.57, 13.12), (-99.8, 27.28), (0.79, -33.16), (78.95, 78.61), (80.92, -39.92), (-95.76, 79.96), (-31.53, 54.57), (-18.47, -31.8), (-96.29, -53.0), (85.06, -45.54), (37.84, 75.75), (-2.38, -40.04), (-37.7, 25.98), (-74.47, 74.73), (85.66, 88.39), (-97.99, 67.34), (-66.24, 47.94), (49.66, -9.73), (66.59, -84.24), (9.82, 22.22), (38.45, -6.1), (-24.67, -77.81), (5.55, 88.13), (85.59, 14.86), (89.28, 89.99), (-47.88, 76.3), (19.9, -47.07), (11.24, 62.22), (16.26, 88.32), (79.24, -44.43), (-99.97, 27.93), (1.01, -60.47), (-51.98, -42.88), (8.71, -23.44), (-82.64, 87.2), (30.8, -8.29), (6.28, 44.43), (25.02, 78.73), (31.69, 62.16), (-36.28, -25.46), (45.35, 77.33), (67.7, -89.31), (-2.42, 71.68), (10.45, 66.92), (-21.02, 30.19)]
    # Compute locations in meters using the block dimension defined as follow
    # Manhattan average block: 750ft x 264ft -> 228m x 80m
    # here we use: 114m x 80m city block
    # src: https://nyti.ms/2GDoRIe "NY Times: Know Your distance"
    data['locations'] = [(l[0], l[1]) for l in _locations]
    data['num_locations'] = len(data['locations'])
    data['time_windows'] =[(0,0), (222, 234), (1378, 1433), (1115, 1136), (1289, 1312), (656, 698), (221, 253), (1086, 1105), (560, 627), (1084, 1143), (1168, 1187), (337, 340), (756, 809), (1316, 1328), (124, 189), (1286, 1313), (154, 221), (21, 78), (834, 853), (735, 816), (386, 425), (1277, 1341), (1202, 1262), (1269, 1336), (1238, 1251), (1045, 1057), (99, 153), (380, 400), (569, 644), (933, 985), (401, 429), (1027, 1073), (959, 1019), (558, 626), (1245, 1269), (603, 642), (1088, 1144),    (127, 172), (764, 785), (473, 517), (875, 890), (597, 641), (460, 484), (23, 97), (403, 463), (299, 348), (1018, 1093), (1078, 1120), (1369, 1396), (487, 503), (1133, 1170)]
    data['demands'] = [(0), (10), (13), (22), (50), (6), (13), (3), (43), (8), (8), (10), (13), (25), (18), (39), (30), (16), (41), (43), (28), (40), (19), (26), (27), (45), (30), (10), (15), (44), (13), (33), (48), (13), (5), (6), (8), (23), (35), (35), (42), (27), (41), (33), (26), (38), (14), (28), (16), (30), (14)]
    data['time_per_demand_unit'] = [(0), (2), (3), (5), (10), (2), (3), (1), (9), (2), (2), (3), (3), (5), (4), (8), (7), (4), (9), (9), (6), (9), (4), (6), (6), (9), (7), (2), (3), (9), (3), (7), (10), (3), (1), (2), (2), (5), (8), (7), (9), (6), (9), (7), (6), (8), (3), (6), (4), (7), (3)]
    data['num_vehicles'] = 20
    data['vehicle_capacity'] = 80
    data['depot'] = 0
    return data


#######################
# Problem Constraints #
#######################
def euclidean_distance(position_1, position_2):
    """Computes the Euclidean distance between two points"""
    return (
        abs(math.sqrt((pow(position_1[0] - position_2[0],2))+(pow(position_1[1] - position_2[1],2))))
        )


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


def create_demand_evaluator(data):
    """Creates callback to get demands at each location."""
    _demands = data['demands']

    def demand_evaluator(manager, node):
        """Returns the demand of the current node"""
        return _demands[manager.IndexToNode(node)]

    return demand_evaluator


def add_capacity_constraints(routing, data, demand_evaluator_index):
    """Adds capacity constraint"""
    capacity = 'Capacity'
    routing.AddDimension(
        demand_evaluator_index,
        0,  # null capacity slack
        data['vehicle_capacity'],
        True,  # start cumul to zero
        capacity)


def create_time_evaluator(data):
    """Creates callback to get total times between locations."""

    def service_time(data, node):
        """Gets the service time for the specified location."""
        return data['time_per_demand_unit'][node]
    def travel_time(data, from_node, to_node):
        """Gets the travel times between two locations."""
        if from_node == to_node:
            travel_time = 0
        else:
            travel_time = euclidean_distance(data['locations'][from_node], data[
                'locations'][to_node])
        return travel_time

    _total_time = {}
    # precompute total time to have time callback in O(1)
    for from_node in xrange(data['num_locations']):
        _total_time[from_node] = {}
        for to_node in xrange(data['num_locations']):
            if from_node == to_node:
                _total_time[from_node][to_node] = 0
            else:
                _total_time[from_node][to_node] = int(
                    service_time(data, from_node) + travel_time(
                        data, from_node, to_node))

    def time_evaluator(manager, from_node, to_node):
        """Returns the total time between the two nodes"""
        return _total_time[manager.IndexToNode(from_node)][manager.IndexToNode(
            to_node)]

    return time_evaluator


def add_time_window_constraints(routing, manager, data, time_evaluator_index):
    """Add Global Span constraint"""
    time = 'Time'
    horizon = 1500
    routing.AddDimension(
        time_evaluator_index,
        horizon,  # allow waiting time
        horizon,  # maximum time per vehicle
        False,  # don't force start cumul to zero since we are giving TW to start nodes
        time)
    time_dimension = routing.GetDimensionOrDie(time)
    # Add time window constraints for each location except depot
    # and 'copy' the slack var in the solution object (aka Assignment) to print it
    for location_idx, time_window in enumerate(data['time_windows']):
        if location_idx == 0:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
        routing.AddToAssignment(time_dimension.SlackVar(index))
    # Add time window constraints for each vehicle start node
    # and 'copy' the slack var in the solution object (aka Assignment) to print it
    for vehicle_id in xrange(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(data['time_windows'][0][0],
                                                data['time_windows'][0][1])
        routing.AddToAssignment(time_dimension.SlackVar(index))
        # Warning: Slack var is not defined for vehicle's end node
        #routing.AddToAssignment(time_dimension.SlackVar(self.routing.End(vehicle_id)))


###########
# Printer #
###########
def print_solution(data, manager, routing, assignment):  # pylint:disable=too-many-locals
    """Prints assignment on console"""
    print('Objective: {}'.format(assignment.ObjectiveValue()))
    total_distance = 0
    total_load = 0
    total_time = 0
    capacity_dimension = routing.GetDimensionOrDie('Capacity')
    time_dimension = routing.GetDimensionOrDie('Time')
    for vehicle_id in xrange(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        distance = 0
        while not routing.IsEnd(index):
            load_var = capacity_dimension.CumulVar(index)
            time_var = time_dimension.CumulVar(index)
            slack_var = time_dimension.SlackVar(index)
            plan_output += ' {0} Load({1}) Time({2},{3}) Slack({4},{5}) ->'.format(
                manager.IndexToNode(index),
                assignment.Value(load_var),
                assignment.Min(time_var),
                assignment.Max(time_var),
                assignment.Min(slack_var), assignment.Max(slack_var))
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            distance += routing.GetArcCostForVehicle(previous_index, index,
                                                     vehicle_id)
        load_var = capacity_dimension.CumulVar(index)
        time_var = time_dimension.CumulVar(index)
        slack_var = time_dimension.SlackVar(index)
        plan_output += ' {0} Load({1}) Time({2},{3})\n'.format(
            manager.IndexToNode(index),
            assignment.Value(load_var),
            assignment.Min(time_var), assignment.Max(time_var))
        plan_output += 'Distance of the route: {0}m\n'.format(distance)
        plan_output += 'Load of the route: {}\n'.format(
            assignment.Value(load_var))
        plan_output += 'Time of the route: {}\n'.format(
            assignment.Value(time_var))
        print(plan_output)
        total_distance += distance
        total_load += assignment.Value(load_var)
        total_time += assignment.Value(time_var)
    print('Total Distance of all routes: {0}m'.format(total_distance))
    print('Total Load of all routes: {}'.format(total_load))
    print('Total Time of all routes: {0}min'.format(total_time))


########
# Main #
########
def main():
    """Entry point of the program"""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager
    manager = pywrapcp.RoutingIndexManager(data['num_locations'],
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model
    routing = pywrapcp.RoutingModel(manager)

    # Define weight of each edge
    distance_evaluator_index = routing.RegisterTransitCallback(
        partial(create_distance_evaluator(data), manager))
    routing.SetArcCostEvaluatorOfAllVehicles(distance_evaluator_index)

    # Add Capacity constraint
    demand_evaluator_index = routing.RegisterUnaryTransitCallback(
        partial(create_demand_evaluator(data), manager))
    add_capacity_constraints(routing, data, demand_evaluator_index)

    # Add Time Window constraint
    time_evaluator_index = routing.RegisterTransitCallback(
        partial(create_time_evaluator(data), manager))
    add_time_window_constraints(routing, manager, data, time_evaluator_index)

    # Setting first solution heuristic (cheapest addition).
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.local_search_metaheuristic = (
    routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = 30
    search_parameters.log_search = True
    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)
    print_solution(data, manager, routing, assignment)


if __name__ == '__main__':
    main()
