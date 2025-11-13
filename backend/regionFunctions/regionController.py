from fastapi import HTTPException, status

from backend.db import supabase
from data_management import data_extraction

def add_region(lat: float, long: float, radius: float, net_type: str):
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
        return {"ok": True, "details": "Inserted nodes and edges"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to add region: {e}")