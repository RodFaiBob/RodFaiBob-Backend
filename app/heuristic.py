import math
import heapq

class Station():
    def __init__(self, id, lat, long):
        self.id = id
        self.lat = lat
        self.long = long
        self.edges = {}
    
    def addEdge(self, node, cost):
        if not isinstance(node, Station):
            raise ValueError("The node must be an instance of the Station class.")
        
        self.edges[node] = cost
        node.edges[self] = cost
    
    def __sub__(self, other):
        if not isinstance(other, Station):
            raise Exception('this method can not be done with different class') 
        
        R = 6371 
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
 
def a_star(start, goal):
    open_list = []
    
    #intialize priority queue
    #push (f(n), station) to the open lsit
    #f(n) = g(n) + h(n) 
    f_start = 0 + (goal-start)
    heapq.heappush(open_list, (f_start, start))
    
    g_score = {start: 0}  # Cost from start to current station
    came_from = {}  # To reconstruct the path
    
    while open_list:
        # cheapest path first
        _, current = heapq.heappop(open_list)
        
        # if goal is found return path and cost
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, g_score[goal]
        
        # add neighbors
        for neighbor, cost in current.edges.items():
            tentative_g_score = g_score[current] + cost
            
            # if never visit or cheaper
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + (neighbor - goal)
                
                # push to priority queue
                heapq.heappush(open_list, (f_score, neighbor))
    
    return None, float('inf')


# Line A Station
A = Station("A", 34.0522, -118.2437) 
B = Station("B", 34.0523, -118.2438)  
C = Station("C", 34.0524, -118.2439)  
D = Station("D", 34.0525, -118.2440)  
E = Station("E", 34.0526, -200.2441)  

# Line B Station
F = Station("F", 35.0522, -119.2437) 
G = Station("G", 35.0523, -119.2438)
H = Station("H", 35.0524, -119.2439)
I = Station("I", 35.0525, -119.2440)
J = Station("J", 35.0526, -119.2441)

# Line C Station
K = Station("K", 36.0522, -120.2437) 
L = Station("L", 36.0523, -120.2438)
M = Station("M", 36.0524, -120.2439)
N = Station("N", 36.0525, -120.2440)
O = Station("O", 36.0526, -120.2441)

# Line A
A.addEdge(B, 2)
A.addEdge(C, 10)
A.addEdge(D, 15)
A.addEdge(E, 20)
B.addEdge(C, 5)
B.addEdge(D, 10)
B.addEdge(E, 15)
C.addEdge(D, 5)
C.addEdge(E, 10)
D.addEdge(E, 5)

# Line B
F.addEdge(G, 5)
F.addEdge(H, 10)
F.addEdge(I, 15)
F.addEdge(J, 20)
G.addEdge(H, 5)
G.addEdge(I, 10)
G.addEdge(J, 15)
H.addEdge(I, 5)
H.addEdge(J, 10)
I.addEdge(J, 5)

# Line C 
K.addEdge(L, 5)
K.addEdge(M, 10)
K.addEdge(N, 15)
K.addEdge(O, 20)
L.addEdge(M, 5)
L.addEdge(N, 10)
L.addEdge(O, 15)
M.addEdge(N, 5)
M.addEdge(O, 10)
N.addEdge(O, 5)


C.addEdge(H, 0)
I.addEdge(L, 0)


# Find the path from A to L
path, cost = a_star(A, L)
if path:
    print("Path:", path)
    print("Cost:", cost)
else:
    print("No path found.")

