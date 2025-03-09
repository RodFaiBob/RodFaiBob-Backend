import os
from fastapi import APIRouter, HTTPException,BackgroundTasks
from fastapi.responses import FileResponse
from app.search.search import  A_star, BFS
from app.utils.csv_reader import STATIONS
from app.utils.graph_animation import save_animation
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
    
    path, cost, runtime, cpu, _, _ = A_star(start_station, goal_station)
    
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
    
    path, cost, runtime, cpu, _, _ = BFS(start_station, goal_station)

    if path:
        return {"path": [station.id for station in path], "cost": cost, "runtime" : runtime, "cpu" : cpu}
    else:
        raise HTTPException(status_code=404, detail="No path found.")

@router.get("/nodes")
async def getNodes():
    return {"nodes": [node.toDict() for _, node in STATIONS.items()]}

@router.get("/video/heuristic")
async def get_video(start: str, goal: str):
    start_station = STATIONS.get(start)
    goal_station = STATIONS.get(goal)
    
    if not start_station or not goal_station:
        raise HTTPException(status_code=404, detail="Station not found.")
    
    video_path = f"video/heuristic/{start}_{goal}.mp4"
    
    if os.path.exists(video_path):
        return FileResponse(video_path)
    else:
        return {"error": "Video file not found"}
    
@router.get("/video/blind")
async def get_video(start: str, goal: str):
    start_station = STATIONS.get(start)
    goal_station = STATIONS.get(goal)
    
    if not start_station or not goal_station:
        raise HTTPException(status_code=404, detail="Station not found.")
    
    video_path = f"video/blind/{start}_{goal}.mp4"
    
    if os.path.exists(video_path):
        return FileResponse(video_path)
    else:
        return {"error": "Video file not found"}



@router.get("/video/heuristic/gen")
async def gen_video(start: str, goal: str, background_tasks: BackgroundTasks):
    start_station = STATIONS.get(start)
    goal_station = STATIONS.get(goal)

    if not start_station or not goal_station:
        raise HTTPException(status_code=404, detail="Station not found.")

    path, _, _, _, nodes, edges = A_star(start_station, goal_station)

    # Ensure the directory exists
    video_dir = os.path.abspath("video/heuristic")  # Ensure absolute path
    if not os.path.exists(video_dir):
        os.makedirs(video_dir, exist_ok=True)

    video_path = os.path.join(video_dir, f"{start}_{goal}.mp4")

    # If the file already exists, return success without regenerating
    if os.path.exists(video_path):
        return {"status": "ok"}

    try:
        background_tasks.add_task(save_animation(path, nodes, edges, video_path))
        return {"status": "ok"}
    except Exception as e:
        print(f"Error saving file: {e}")
        if os.path.exists(video_path):
            os.remove(video_path)
            print(f"Corrupted file '{video_path}' has been removed.")
        return {"status": "error", "message": str(e)}

@router.get("/video/blind/gen")
async def gen_video(start: str, goal: str,background_tasks: BackgroundTasks):
    start_station = STATIONS.get(start)
    goal_station = STATIONS.get(goal)

    if not start_station or not goal_station:
        raise HTTPException(status_code=404, detail="Station not found.")

    path, _, _, _, nodes, edges = BFS(start_station, goal_station)

    # Ensure the directory exists
    video_dir = os.path.abspath("video/blind")
    if not os.path.exists(video_dir):
        os.makedirs(video_dir, exist_ok=True)

    video_path = os.path.join(video_dir, f"{start}_{goal}.mp4")

    # If the file already exists, return success without regenerating
    if os.path.exists(video_path):
        return {"status": "ok"}

    try:
        background_tasks.add_task(save_animation(path, nodes, edges, video_path))
        return {"status": "ok"}
    except Exception as e:
        print(f"Error saving file: {e}")
        if os.path.exists(video_path):
            os.remove(video_path)
            print(f"Corrupted file '{video_path}' has been removed.")
        return {"status": "error", "message": str(e)}
