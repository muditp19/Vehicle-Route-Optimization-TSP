# Vehicle-Route-Optimization-TSP
OR-Tools is an open source software suite for optimization, tuned for tackling the world's toughest problems in vehicle routing, flows, integer and linear programming, and constraint programming.
An example of a node-routing problem is vehicle routing. Suppose that a company needs to deliver packages to various locations, using a fleet of vehicles. 
In the graph for this problem, nodes represent locations, and arcs represent routes between them. Each arc has a weight, corresponding to the cost of traveling that route. The problem: find a set of paths in the graph (corresponding to delivery routes for each vehicle) that includes every destination while minimizing the total cost. This differs from the arc-routing problem because the paths don't have to traverse every arc, just include every node.

One of the most important things in using the OR-Tools is to use the right searching strategy and the right parameters to stop the search. Search limits terminate the solver after it reaches a specified limit, such as the maximum length of time, or number of solutions found. You can set a search limit through the solver's search parameters.

Results
Without time windows
VEHICLE NUMBER	ROUTE: NODE (LOAD)	DISTANCE OF THE ROUTE (MILE)	LOAD OF THE ROUTE
1	0 (0) → 32 (48) → 37 (71) → 0 (71)	134	71
2	0 (0) → 26 (30) → 29 (74) → 0 (74)	175	74
3	0 (0) → 49 (30) → 42 (71) → 0 (71)	133	71
4	
0 (0) → 40 (42) → 3 (64) → 48 (80) → 0 (80)
	282	80
5	0 (0) → 44 (26) → 30 (39) → 20 (67) → 9 (75) → 0 (75)	257	75
6	0  (0) → 38 (35) → 14  (53) → 27 (63) → 17 (79) → 0 (79)	270	79
7	0 (0) → 46 (14) → 16 (44) → 43 (77) → 0 (77)	191	77
8	0 (0) → 33 (13) → 34 (18) → 28 (33) → 31 (66) → 12 (79) → 0 (79)	243	79
9	0 (0) → 35 (6) → 15 (45) → 10 (53) → 23 (79) → 0 (79)	194	79
10	0 (0) → 22 (19) → 4 (69) → 11 (79) → 0 (79)	248	79
11	0 (0) → 1 (10) → 47 (38) → 24 (65) → 6 (78) → 0 (78)	368	78
12	0 (0) → 18 (41) → 45 (79) → 0 (79)	140	79
13	0 (0) → 25 (45) → 41 (72) → 0 (72)	92	72
14	0 (0) → 8 (43) → 39 (78) → 0 (78)	70	78
15	0 (0) → 2 (13) → 50 (27) → 19 (70) → 5 (76) → 0 (76)	224	76
TOTAL DISTANCE OF ALL ROUTES (MILE)	3,314
TOTAL LOAD OF ALL ROUTES	1,223
TOTAL COST ($) : DISTANCE TRAVELLED + TRUCK USED	19,314

With Time windows

VEHICLE NUMBER	ROUTE: NODE (LOAD) / TIME / SLACK	DISTANCE OF THE ROUTE (MILE)	LOAD OF THE ROUTE	TIME OF THE ROUTE (MIN)
1	0 (0) / (0,0) / (566,610) → 41 (0) / (597,641) / (342,428) → 47 (27) / (1078,1120) / (87,141) → 13 (55) / (1316,1328) / (0,143) → 0 (80) / (1357,1500)	259	80	1357
2	0 (0) / (0,0) / (213,216) → 11 (0) / (337,340) / (944,970) → 4 (10) / (1289,1312) / (0,34) → 2 (60) / (1399,1433) / (0,77) → 0 (73) / (1423,1500)	247	73	1423
3	0 (0) / (0,0) / (420,436) → 49 (0) / (487,503) / (44,128) → 33 (30) / (558,626) / (84,205) → 12 (43) / (756,809) / (295,385) → 50 (56) / (1133,1170) / (0,328) → 0 (70) /  (1172,1500)	176	70	1172
4	0 (0) / (0,0) / (847,899) → 29 (0) / (933,985) / (232,351) → 23 (44) / (1269, 1336) / (0,175) → 0 (70) / (1325,1500)	179	70	1325
5	0 (0) / (0,0) / (131,163) → 6 (0) / (221,253) / (69,119) → 30 (13) / (401,419) / (0,18) → 20 (26) / (407,425) / (642,719) → 9 (54) / (1084,1143) / (0,303) → 0 (62) / (1197,1500)	291	62	1197
6	0 (0) / (0,0) / (67,112) → 37 (0) / (127,172) / (8,65) → 1 (23) / (222,234) / (119,151) → 27 (33) / (380,400) / (318,359) → 38 (43) / (764,785) / (0,661) → 0 (78) / (839,1500)	233	78	839
7	0 (0) / (0,0) / (0,15) → 43 (0) / (82,97) / (444,534) → 28 (33) / (569,644) / (459,555) → 3 (48) / (1115,1136) / (0,298) → 0 (70) / (1202,1500)	194	70	1202
8	0 (0) / (0,0) / (448,492) → 39 (0) / (473,517) / (24,135) → 8 (35) / (560,627) / (0,898) → 0 (78) / (602,1500)	70	78	602
9	0 (0) / (0,0) / (70,137) → 16 (0) / (154,221) / (783,925) → 46 (30) / (1018,1093) / (118,217) → 34 (44) / (1245,1269) / (74,125) → 48 (49) / (1369,1396) / (0,56) → 0 (65) / (1444,1500)	218	65	1444
10	0 (0) / (0,0) / (334,379) → 44 (0) / (403,448) / (0,45) → 42 (26) / (460,484) / (0,987) → 0 (67) / (513,1500)	143	67	513
11	0 (0) / (0,0) / (513,552) → 35 (0) / (603,642) / (520,578) → 10 (6) / (1168,1187) / (3,35) → 24 (14) / (1238, 1251) / (0,27) → 15 (41) / (1286,1313) / (0,110) → 0 (80) / (1390,1500)	278	80	1390
12	0 (0) / (0,0) / (61,115) → 26 (0) / (99,153) / (845,911) → 25 (30) / (1045,1057) / (0,422) → 0 (75) / (1078,1500)	102	75	1078
13	0 (0) / (0,0) / (755,770) → 40 (0) / (875,890) / (92,153) → 31 (42) / (1027,1073) / (0,376) → 0 (75) / (1124,1500)	246	75	1124
14	0 (0) / (0,0) / (0,38) → 17 (0) / (40,78) / (854,952) → 32 (16) / (959,1019) / (0,480) → 0 (64) / (1020,1500)	114	64	1020
15	0 (0) / (0,0) / (596,638) → 5 (0) / (656,698) / (0,100) → 19 (6) / (735,816) / (349,490) → 22 (49) / (1202,1262) / (0,213) → 0 (68) / (1287,1500)	227	68	1287
16	0 (0) / (0,0) / (15,80) → 14 (0) / (!24,189) / (813,897) → 7 (18) / (1086,1105) / (0,57) → 36 (21) / (1088,1144) / (92,212) → 21 (29) / (1277,1341) / (0,96) → 0 (69) / (1404,1500)	346	69	1404
17	0 (0) / (0,0) / (255,304) → 45 (0) / (299,348) / (427,495) → 18 (38) / (834,853) / (0,612) → 0 (79) / (888,1500)	140	79	888
TOTAL DISTANCE OF ALL ROUTES (MILE)	3,463
TOTAL LOAD OF ALL ROUTES	1,223
TOTAL TIME OF ALL ROUTES (MIN)	19,265
TOTAL COST ($) : DISTANCE TRAVELLED + TRUCK USED	20,463

