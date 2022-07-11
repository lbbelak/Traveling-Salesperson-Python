import json
import sys
from math import radians, cos, sin, asin, sqrt, inf
from typing import Optional , List, Tuple

Earth_Radius = 6371



def calculate_distance(first, second):
    gps1 = (radians(first[1]), radians(first[2]))
    gps2 = (radians(second[1]), radians(second[2]))
    dif_lat = gps1[0] - gps2[0]
    dif_lon = gps1[1] - gps2[1]
    a = sin(dif_lat / 2) ** 2 + cos(gps1[0]) * cos(gps2[0]) * sin(dif_lon / 2) ** 2
    c = 2 * asin(sqrt(a))
    result = c * Earth_Radius
    return result


def get_distances(cities):
    new_cities = []
    for i, city in enumerate(cities):
        one = [city[0]]
        two = []
        for index in range(0, len(cities)):
            lenght = calculate_distance(cities[i], cities[index])
            two.append(cities[index][0])
            two.append(lenght)
            one.append(two)
            two = []
        new_cities.append(one)
    return (new_cities)

class Graph:
   
    def __init__(self, size: int):
        self.size = size
        self.succs: List[List[Tuple[int, int]]] = \
            [[] for _ in range(size)]


class Vertex:
   
    def __init__(self, name: str):
        self.name = name
        self.succs: List[Tuple[Vertex, int]] = []
        self.flag: Optional[int] = 0
        self.to_finish: int = 0

def make_graph(all_paths):
    graph = Graph(len(all_paths))
    for i, vertex in enumerate(all_paths):
        city = Vertex(vertex[0])
        graph.succs[i] = city
    return graph


def make_vertices(all_paths, graph):
    for i, vertex in enumerate(all_paths):
        for neigbor in range(1, len(vertex)):
            x = graph.succs[i]
            x.succs.append(((graph.succs[neigbor - 1], vertex[neigbor][1])))
            x.to_finish = graph.succs[i].succs[0][1]


def DFS(graph, actual, layer, candidate_path, all_candidates):
    min_dist = 0
    actual.flag = 1
    change = False
    candidate_path[layer] = actual

    for vertex, distance in actual.succs:
        if vertex.flag == 0 and vertex != graph.succs[0] and vertex != actual:
            change = True
            x, candidate_path, all_candidates = DFS(graph, vertex, layer + 1, candidate_path.copy(), all_candidates)
            x += distance

            if min_dist == 0:

                min_dist = x
            elif x <= min_dist:
                min_dist = x
    if not change:
        all_candidates.append(candidate_path)
        min_dist += actual.to_finish
    actual.flag = 0
    return min_dist, candidate_path, all_candidates


def find_path(all_candidates,minimum):

    for path in all_candidates:
        route = []
        total = 0
        for i in range(0, len(path)):
            if i + 1 < len(path):
                find = path[i+1].name
                for x, distance in path[i].succs:
                    if x.name == find:
                        total += distance
                        route.append(distance)
            else:
                total += path[i].succs[0][1]
                route.append(path[i].succs[0][1])
        if total == minimum:
            return path,route


def main(file_path: str):
    cities = []
    with open(file_path, 'r') as f:
        data = json.load(f)
        for i, location in enumerate(data):
            city = [location['name'], location['latitude'], location['longitude']]
            cities.append(city)
    all_paths = get_distances(cities)
    graph = make_graph(all_paths)
    make_vertices(all_paths, graph)
    all_candidates = []
    minimum, x, all_candidates = (DFS(graph, graph.succs[0], 0, [None, None, None, None, None], all_candidates))
    path,distance = find_path(all_candidates, minimum)
    for i, city in enumerate(path):
        print(city.name)
        print(distance[i])
    print(path[0].name)
    print(f"Total path is {minimum} km")
    return minimum

if __name__ == "__main__":
    main(sys.argv[1])