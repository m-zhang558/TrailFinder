import math

from fastapi import HTTPException, status, Response
from fastapi.responses import JSONResponse

from backend.db import supabase
import backend.routing.routingFunctions as routingFunctions

async def calculate_route(startLat: float, startLong: float, endLat: float, endLong: float, distance: float):
    # check if distance parameter is greater than distance between start and end
    start_to_end = math.sqrt((startLat - endLat) ** 2 + (startLong - endLong) ** 2)
    if start_to_end > distance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not enough distance to reach end!")

    # get all nodes and edges in region and build networkX graph
    try:
        nodes = supabase.rpc("get_nodes", {"lat": startLat, "lon": startLong, "radius": distance}).execute()
        edges = supabase.rpc("get_edges", {"lat": startLat, "lon": startLong, "radius": distance}).execute()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to get region data: {e}")
    graph = routingFunctions.build_graph(nodes, edges)

    # get nearest node to start and nearest node to end
    try:
        start = supabase.rpc("get_nearest", {"lat": startLat, "lon": startLong}).execute()
        end = supabase.rpc("get_nearest", {"lat": endLat, "lon": endLong}).execute()
        print(start.data)
        start_id = start.data[0]["id"]
        end_id = end.data[0]["id"]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to obtain start or end: {e}")
    #start_id = 0
    #end_id = 1
    print("start_id: " + start_id)
    print("end_id: " + end_id)

    # perform graph traversal
    path = routingFunctions.get_route(start_id, end_id, graph)

    return {
        "path": path
    }

