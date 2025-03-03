import math

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
