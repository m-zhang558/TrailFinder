from fastapi import HTTPException, status, Request, Response

from backend.db import supabase
from data_management import data_extraction

def add_region(request: Request) -> Response:
    lat = request["lat"]
    if not lat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Latitude is required")
    long = request["long"]
    if not long:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Longitude is required")
    radius = request["radius"]
    if not radius:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Radius is required")
    net_type = request["net_type"]
    if not net_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Net type is required")
    coords = (lat, long)
    graph = data_extraction.get_graph(coords, radius, net_type)
    nodes, edges = data_extraction.convert_graph(graph)

    if nodes.empty() or edges.empty():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No nodes or edges found")

    n_json = nodes.to_json(na='null', drop_id=True)
    e_json = edges.to_json(na='null', drop_id=True)

    try:
        supabase.table("nodes").insert(n_json).execute()
        supabase.table("edges").insert(e_json).execute()
        return Response(status_code=status.HTTP_201_CREATED)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to add region: {e}")