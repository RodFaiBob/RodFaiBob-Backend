import heapq
import time
import psutil
from typing import List, Tuple, Union
from app.model.station import Station

def BFS(start: Station, goal: Station) -> Tuple[Union[List[Station], None], float, float, float]:
    visited = set()
    queue = [[start]]

    start_time = time.time()
    start_cpu = psutil.cpu_percent(interval=None)

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
                    return None, float('inf'), None, None

                sum_cost += cost

                end_time = time.time()
                end_cpu = psutil.cpu_percent(interval=None)

                runtime = end_time - start_time
                avg_cpu = (start_cpu + end_cpu) / 2

            return path, sum_cost, runtime, avg_cpu

        if node not in visited:
            visited.add(node)
            neighbors = node.getNeighbor()
            
            for neighbor in neighbors:
                new_path = path + [neighbor]
                queue.append(new_path)
    
    return None, float('inf'), None, None

def A_star(start: Station, goal: Station) -> Tuple[Union[List[Station], None], float, float, float]:
    open_list = []
    start_time = time.time()
    start_cpu = psutil.cpu_percent(interval=None)

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

            end_time = time.time()
            end_cpu = psutil.cpu_percent(interval=None)

            runtime = end_time - start_time
            avg_cpu = (start_cpu + end_cpu) / 2

            return path, g_score[goal], runtime, avg_cpu
        
        for neighbor, cost in current.edges.items():
            tentative_g_score = g_score[current] + cost
            
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + (neighbor - goal)
                
                heapq.heappush(open_list, (f_score, neighbor))
    
    return None, float('inf'), None, None