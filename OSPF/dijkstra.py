# -*- coding: utf-8 -*-

def get_neighbors(g, nodes, target):
    neighbors = []
    for node in nodes:
        if g[target].get(node, False) != False:
            neighbors.append(node)
    return neighbors


def dijkstra_algorithm(network, start_node, routers):
    path = {} #s ave all previous path
    unvisited_routers = routers.copy() #list of all routers
    
    shortest_path = {}
    for router in unvisited_routers:
        shortest_path[router] = float('inf')
    shortest_path[start_node] = 0
    
    while unvisited_routers:
        curr_min = None
        for router in unvisited_routers:
            if curr_min == None:
                curr_min = router
            elif shortest_path[router] < shortest_path[curr_min]:
                curr_min = router
        neighbors = get_neighbors(network,list(network.keys()), curr_min)
        for neighbor in neighbors:
            temp_val = shortest_path[curr_min] + network[curr_min][neighbor]
            if temp_val < shortest_path[neighbor]:
                shortest_path[neighbor] = temp_val
                path[neighbor] = curr_min
        unvisited_routers.remove(curr_min)
    return path, shortest_path

def get_next_hop(network, start_node, path):
    neighbors = get_neighbors(network, list(network.keys()), start_node)
    p = path.copy()
    for router in path:
        if path[router] != start_node and path[router] not in neighbors:
            curr = path[router]
            while curr not in neighbors:
                curr = path[curr]
            p[router] = curr
    return p


nodes = ['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7']
n  = {'r1': {'r2' : 1}, 
      'r2': {'r1': 1, 'r3': 1},
      'r3': {'r2': 1, 'r4': 1, 'r5': 1},
      'r4': {'r3': 1, 'r6': 1},
      'r5': {'r3': 1, 'r6': 1},
      'r6': {'r4': 1, 'r5': 1}}


n1  = {'r1': {'r2' : 1}, 
      'r2': {'r1': 1, 'r3': 1},
      'r3': {'r2': 1, 'r4': 1, 'r5': 1},
      'r4': {'r3': 1, 'r7': 1},
      'r5': {'r3': 1, 'r6': 1},
      'r6': {'r4': 1, 'r5': 1},
      'r7': {'r4': 1, 'r6': 1}}

'''
r1-r2-r3-r4-r7-r6
        -r5-r6
'''

p, sp = dijkstra_algorithm(n1, 'r1', nodes)
u1 = get_next_hop(n1, 'r1', p)

p2, sp2 = dijkstra_algorithm(n1, 'r2', nodes)
u2 = get_next_hop(n1, 'r2', p2)

p3, sp3 = dijkstra_algorithm(n1, 'r3', nodes)
u3 = get_next_hop(n1, 'r3', p3)

p4, sp4 = dijkstra_algorithm(n1, 'r4', nodes)
u4 = get_next_hop(n1, 'r4', p4)

p5, sp5 = dijkstra_algorithm(n1, 'r5', nodes)
u5 = get_next_hop(n1, 'r5', p5)

p6, sp6 = dijkstra_algorithm(n1, 'r6', nodes)
u6 = get_next_hop(n1, 'r6', p6)

p7, sp7 = dijkstra_algorithm(n1, 'r7', nodes)
u7 = get_next_hop(n1, 'r7', p7)
