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
            temp_val = shortest_path[curr_min] + network[curr_min][neighbor][1]
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

def get_host(network, next_hop, start, shortest_path):
    dic = {}
    for router in network:
        if (router in next_hop):
            if router == start:
                for k,v in network[router].items():
                    if v[0] == 'host':
                        dic[k] = [k]
            else:
                for k,v in network[router].items():
                    if v[0] == 'host':
                        if (next_hop[router] == start):
                            dic[k] = [router, shortest_path[router] + 2]
                        else:
                            dic[k] = [next_hop[router], shortest_path[router] + 2]
    return dic


def update_table(network, router, start_node):
    path, shortest_path = dijkstra_algorithm(network, start_node, router)
    next_hop = get_next_hop(network, start_node, path)
    table = get_host(network, next_hop, start_node, shortest_path)
    return table