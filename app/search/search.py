import heapq
import time
import psutil
from typing import List, Tuple, Union
from app.model.station import Station

def getCostByPath(path):
  sum_cost = 0
  for i in range(len(path)):
    station = path[i]

    if i >= len(path) - 1:
      break

    cost = station.getCostToNode(path[i + 1])

    sum_cost += cost
  return sum_cost


def BFS(start: Station, goal: Station) -> Tuple[Union[List[Station], None], float, float, float, List[Station], List[Tuple[Station, Station]]]:
    visited = set()
    queue = [[start]]

    start_time = time.time()
    start_cpu = psutil.cpu_percent(interval=None)
    
    visited_edges = []
    
    while queue:
        path = queue.pop(0)
        node = path[-1] 
    
        if node != start:
            visited_edges.append((path[-2], node))

        if node == goal:
            current_path = path
            currnet_cost = getCostByPath(path)
            for sub_path in queue:
                if sub_path[-1] == goal:
                    target_cost = getCostByPath(p)
                    if target_cost < currnet_cost:
                        current_path = sub_path
                        currnet_cost = target_cost

            end_time = time.time()
            end_cpu = psutil.cpu_percent(interval=None)

            runtime = end_time - start_time
            avg_cpu = (start_cpu + end_cpu) / 2
            
            return current_path, currnet_cost, runtime, avg_cpu, list(visited), visited_edges

        if node not in visited:
            visited.add(node)
            neighbors = node.getNeighbor()
            
            for neighbor in neighbors:
                new_path = path + [neighbor]
                queue.append(new_path)
    
    return None, float('inf'), None, None, None, None


def A_star(start: Station, goal: Station) -> Tuple[Union[List[Station], None], float, float, float, List[Station], List[Tuple[Station, Station]]]:
    open_list = []
    start_time = time.time()
    start_cpu = psutil.cpu_percent(interval=None)

    f_start = 0 + (goal - start)
    heapq.heappush(open_list, (f_start, start))
    
    g_score = {start: 0}  # Cost from start to current station
    came_from = {}  # To reconstruct the path
    edges_visited = []
    nodes_visited = []
    
    while open_list:
        _, current = heapq.heappop(open_list)
        
        # visted nodes and edges for visualization
        if current != start:
            edges_visited.append((came_from[current], current))
        nodes_visited.append(current)
        
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

            return path, g_score[goal], runtime, avg_cpu, nodes_visited, edges_visited
        
        for neighbor, cost in current.edges.items():
            tentative_g_score = g_score[current] + cost
            
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + (neighbor - goal)
                
                heapq.heappush(open_list, (f_score, neighbor))
    
    return None, float('inf'), None, None, None, None