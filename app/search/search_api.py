from fastapi import APIRouter, HTTPException
from app.search.search import  A_star, BFS
from app.utils.csv_reader import STATIONS
from pydantic import BaseModel


router = APIRouter()

class StationRequest(BaseModel):
    start: str
    goal: str

# A* Endpoint
@router.get("/heuristic")
async def heuristic_path(start: str, goal: str):
    start_station = STATIONS.get(start)
    goal_station = STATIONS.get(goal)
    
    if not start_station or not goal_station:
        raise HTTPException(status_code=404, detail="Station not found.")
    
    path, cost, runtime, cpu = A_star(start_station, goal_station)
    
    if path:
        return {"path": [station.id for station in path], "cost": cost, "runtime" : runtime, "cpu" : cpu}
    else:
        raise HTTPException(status_code=404, detail="No path found.")

# BFS Endpoint
@router.get("/blind")
async def blind(start: str, goal: str):
    start_station = STATIONS.get(start)
    goal_station = STATIONS.get(goal)
    
    if not start_station or not goal_station:
        raise HTTPException(status_code=404, detail="Station not found.")
    
    path, cost, runtime, cpu = BFS(start_station, goal_station)
    
    if path:
        return {"path": [station.id for station in path], "cost": cost, "runtime" : runtime, "cpu" : cpu}
    else:
        raise HTTPException(status_code=404, detail="No path found.")

@router.get("/nodes")
async def getNodes():
    return {"nodes": [node.toDict() for _, node in STATIONS.items()]}