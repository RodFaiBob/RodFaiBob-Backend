from fastapi import APIRouter, HTTPException
from app.search.search import Station, A_star, BFS
from pydantic import BaseModel


# Create a router instance to handle search-related endpoints
router = APIRouter()



stations = {
    "A": Station("A", 34.0522, -118.2437), 
    "B": Station("B", 34.0523, -118.2438),  
    "C": Station("C", 34.0524, -118.2439),  
    "D": Station("D", 34.0525, -118.2440),  
    "E": Station("E", 34.0526, -200.2441),

    "F": Station("F", 35.0522, -119.2437), 
    "G": Station("G", 35.0523, -119.2438),
    "H": Station("H", 35.0524, -119.2439),
    "I": Station("I", 35.0525, -119.2440),
    "J": Station("J", 35.0526, -119.2441),

    "K": Station("K", 36.0522, -120.2437), 
    "L": Station("L", 36.0523, -120.2438),
    "M": Station("M", 36.0524, -120.2439),
    "N": Station("N", 36.0525, -120.2440),
    "O": Station("O", 36.0526, -120.2441),
}

# Line A
stations["A"].addEdge(stations["B"], 2)
stations["A"].addEdge(stations["C"], 10)
stations["A"].addEdge(stations["D"], 15)
stations["A"].addEdge(stations["E"], 20)
stations["B"].addEdge(stations["C"], 5)
stations["B"].addEdge(stations["D"], 10)
stations["B"].addEdge(stations["E"], 15)
stations["C"].addEdge(stations["D"], 5)
stations["C"].addEdge(stations["E"], 10)
stations["D"].addEdge(stations["E"], 5)

# Line B
stations["F"].addEdge(stations["G"], 5)
stations["F"].addEdge(stations["H"], 10)
stations["F"].addEdge(stations["I"], 15)
stations["F"].addEdge(stations["J"], 20)
stations["G"].addEdge(stations["H"], 5)
stations["G"].addEdge(stations["I"], 10)
stations["G"].addEdge(stations["J"], 15)
stations["H"].addEdge(stations["I"], 5)
stations["H"].addEdge(stations["J"], 10)
stations["I"].addEdge(stations["J"], 5)

# Line C 
stations["K"].addEdge(stations["L"], 5)
stations["K"].addEdge(stations["M"], 10)
stations["K"].addEdge(stations["N"], 15)
stations["K"].addEdge(stations["O"], 20)
stations["L"].addEdge(stations["M"], 5)
stations["L"].addEdge(stations["N"], 10)
stations["L"].addEdge(stations["O"], 15)
stations["M"].addEdge(stations["N"], 5)
stations["M"].addEdge(stations["O"], 10)
stations["N"].addEdge(stations["O"], 5)

# Interconnections
stations["C"].addEdge(stations["H"], 0)
stations["I"].addEdge(stations["L"], 0)


# FastAPI Model for Request Data
class StationRequest(BaseModel):
    start: str
    goal: str

# A* Endpoint
@router.post("/heuristic")
async def heuristic_path(request: StationRequest):
    start_station = stations.get(request.start)
    goal_station = stations.get(request.goal)
    
    if not start_station or not goal_station:
        raise HTTPException(status_code=404, detail="Station not found.")
    
    path, cost = A_star(start_station, goal_station)
    
    if path:
        return {"path": [station.id for station in path], "cost": cost}
    else:
        raise HTTPException(status_code=404, detail="No path found.")

# BFS Endpoint
@router.post("/blind")
async def blind_path(request: StationRequest):
    start_station = stations.get(request.start)
    goal_station = stations.get(request.goal)
    
    if not start_station or not goal_station:
        raise HTTPException(status_code=404, detail="Station not found.")
    
    path, cost = BFS(start_station, goal_station)
    
    if path:
        return {"path": [station.id for station in path], "cost": cost}
    else:
        raise HTTPException(status_code=404, detail="No path found.")
