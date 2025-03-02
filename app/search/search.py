import math
import heapq
from typing import List, Tuple, Union

class Station():
    def __init__(self, id: str, lat: float, long: float):
        self.id = id
        self.lat = lat
        self.long = long
        self.edges = {}

    def addEdge(self, node, cost: float):
        if not isinstance(node, Station):
            raise ValueError("The node must be an instance of the Station class.")
        
        self.edges[node] = cost
        node.edges[self] = cost
    
    def __sub__(self, other):
        if not isinstance(other, Station):
            raise Exception('This method cannot be done with a different class')

        R = 6371  # Earth radius in kilometers
        lat1, lon1 = self.lat, self.long
        lat2, lon2 = other.lat, other.long
        
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = R * c
        return distance
    
    def __repr__(self):
        return str(self.id)

    def getNeighbor(self):
        return self.edges
    
    def getCostToNode(self, node):
        if not isinstance(node, Station):
            raise ValueError("The node must be an instance of the Station class.")

        if node not in self.edges:
            return -1
        
        return self.edges[node]

def BFS(start: Station, goal: Station) -> Tuple[Union[List[Station], None], float]:
    visited = set()
    queue = [[start]]

    while queue:
        path = queue.pop(0)
        node = path[-1]

        if node == goal:
            sum_cost = 0
            for n_station in range(len(path) - 1):
                station = path[n_station]

                if not isinstance(station, Station):
                    raise Exception('This method cannot be done with different class')
                
                if station == goal:
                    break

                cost = station.getCostToNode(path[n_station + 1])

                if cost == -1:
                    return None, float('inf')

                sum_cost += cost
            return path, sum_cost

        if node not in visited:
            visited.add(node)
            neighbors = node.getNeighbor()
            
            for neighbor in neighbors:
                new_path = path + [neighbor]
                queue.append(new_path)
    
    return None, float('inf')

def A_star(start: Station, goal: Station) -> Tuple[Union[List[Station], None], float]:
    open_list = []
    
    f_start = 0 + (goal - start)
    heapq.heappush(open_list, (f_start, start))
    
    g_score = {start: 0}  # Cost from start to current station
    came_from = {}  # To reconstruct the path
    
    while open_list:
        _, current = heapq.heappop(open_list)
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, g_score[goal]
        
        for neighbor, cost in current.edges.items():
            tentative_g_score = g_score[current] + cost
            
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + (neighbor - goal)
                
                heapq.heappush(open_list, (f_score, neighbor))
    
    return None, float('inf')