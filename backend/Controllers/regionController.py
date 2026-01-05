from fastapi import HTTPException, status, Response
from fastapi.responses import JSONResponse

import osmnx as ox
import numpy as np

from backend.db import supabase
from data_management import data_extraction
from pydantic import BaseModel

class Region(BaseModel):
    lat: float
    long: float
    radius: float | None = None
    net_type: str | None = None

async def add_region(region: Region) -> Response:
    lat = region.lat
    if not lat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Latitude is required")
    long = region.long
    if not long:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Longitude is required")
    radius = region.radius
    if not radius:
        radius = 500
    net_type = region.net_type
    if not net_type:
        # need to add more thorough check for net_type
        net_type = "walk"
    coords = (lat, long)
    try:
        graph = data_extraction.get_graph(coords, radius, net_type)
    except ox._errors.InsufficientResponseError:
        raise HTTPException(
            status_code=404,
            detail="No map data found for the given location, radius, and network type."
        )
    nodes, edges = data_extraction.convert_graph(graph)

    if nodes.empty or edges.empty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No nodes or edges found")

    n_dict = nodes.to_dict(orient='records')
    e_dict = edges.to_dict(orient='records')

    try:
        supabase.table("nodes").upsert(n_dict, on_conflict="osmid").execute()
        supabase.table("edges").insert(e_dict).execute()
        return Response(status_code=status.HTTP_201_CREATED)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to add region: {e}")


    # Fix adding edges
    # Fix adding duplicates

async def get_region(region) -> Response:
    lat = region.lat
    if not lat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Latitude is required")
    long = region.long
    if not long:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Longitude is required")
    radius = region.radius
    if not radius:
        radius = 1000
    try:
        nodes = supabase.rpc("get_nodes", { "lat": lat, "lon": long, "radius": radius }).execute()
        edges = supabase.rpc("get_edges", { "lat": lat, "lon": long, "radius": radius }).execute()
        print(type(nodes.data))
        print(type(edges.data))
        return JSONResponse(
            status_code=200,
            content={
                "nodes": nodes.data,
                "edges": edges.data
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to add region: {e}")


