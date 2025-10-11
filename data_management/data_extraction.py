import osmnx as ox
import geopandas as gpd
import networkx as nx

"""
retrieves MultiDiGraph of surrounding area from a point
"""
def get_graph(coordinates: tuple[float, float], radius: float, network_type: str="all") -> nx.MultiDiGraph:

    # checks all network types
    VALID_NETWORK_TYPES = {"all", "all_private", "bike", "drive", "drive_service", "walk"}
    if network_type not in VALID_NETWORK_TYPES:
        network_type = "all"

    raw_graph = ox.graph_from_point(center_point=coordinates, dist=radius, dist_type="bbox",
                                    network_type=network_type, truncate_by_edge=True)
    return raw_graph

"""
converts MultiDiGraph to geopandas df and extracts nodes and edges
return: (nodes, edges)
"""
def convert_graph(raw_graph: nx.MultiDiGraph) -> (gpd.GeoDataFrame, gpd.GeoDataFrame):
    return ox.graph_to_gdfs(raw_graph)

