from fastapi import APIRouter, HTTPException
from app.search.search import  A_star, BFS
from app.search.init import stations
from pydantic import BaseModel


# Create a router instance to handle search-related endpoints
router = APIRouter()

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
    
    path, cost, runtime, cpu = A_star(start_station, goal_station)
    
    if path:
        return {"path": [station.id for station in path], "cost": cost, "runtime" : runtime, "cpu" : cpu}
    else:
        raise HTTPException(status_code=404, detail="No path found.")

# BFS Endpoint
@router.post("/blind")
async def blind_path(request: StationRequest):
    start_station = stations.get(request.start)
    goal_station = stations.get(request.goal)
    
    if not start_station or not goal_station:
        raise HTTPException(status_code=404, detail="Station not found.")
    
    path, cost, runtime, cpu = BFS(start_station, goal_station)
    
    if path:
        return {"path": [station.id for station in path], "cost": cost, "runtime" : runtime, "cpu" : cpu}
    else:
        raise HTTPException(status_code=404, detail="No path found.")
