import osmnx as ox
import geopandas as gpd
import networkx as nx
import numpy as np

"""
retrieves MultiDiGraph of surrounding area from a point
"""
def get_graph(coordinates: tuple[float, float], radius: float, network_type: str="all") -> nx.MultiDiGraph:

    # checks all network types
    VALID_NETWORK_TYPES = {"all", "all_private", "bike", "drive", "drive_service", "walk"}
    if network_type not in VALID_NETWORK_TYPES:
        network_type = "all"

    raw_graph = ox.graph_from_point(center_point=coordinates, dist=radius, dist_type="bbox",
                                    network_type=network_type, simplify=False, truncate_by_edge=True)
    return raw_graph

"""
converts MultiDiGraph to geopandas df and extracts nodes and edges
return: (nodes, edges)
"""
def convert_graph(raw_graph: nx.MultiDiGraph) -> (gpd.GeoDataFrame, gpd.GeoDataFrame):
    nodes, edges = ox.graph_to_gdfs(raw_graph)
    nodes = nodes.reset_index().rename(columns={'index': 'osmid'})
    edges = edges.reset_index()

    # drop unwanted cols
    drop_node_cols = ["ref", "name", "street_count", "highway", "amenity", "shop"]
    nodes = nodes.drop(columns=drop_node_cols, errors="ignore")
    drop_cols = [
        "maxspeed", "lanes", "bridge", "service", "junction",
        "access", "tunnel", "width", "ref", "oneway", "reversed",
        "key", "osmid:tidy", "foot", "cycleway", "surface"
    ]
    print("EDGE COLUMNS BEFORE DROP:", edges.columns.tolist())
    edges = edges.drop(columns=drop_cols, errors="ignore")
    print("EDGE COLUMNS AFTER DROP:", edges.columns.tolist())

    # get rid of list cols
    if "osmid" in edges.columns:
        edges["osmid"] = edges["osmid"].apply(lambda x: x[0] if isinstance(x, list) else x)
    if "geometry" in nodes.columns:
        nodes["geometry"] = nodes["geometry"].apply(lambda g: g.wkt if g else None)
    if "geometry" in edges.columns:
        edges["geometry"] = edges["geometry"].apply(lambda g: g.wkt if g else None)

    # replace nans with None
    nodes = nodes.replace(np.nan, None)
    edges = edges.replace(np.nan, None)
    return nodes, edges
