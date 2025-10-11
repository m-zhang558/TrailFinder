import geopandas as gpd
import pandas as pd
import psycopg2
from numpy.f2py.auxfuncs import throw_error


class DataProcessing:
    def __init__(self, nodes, edges):
        self.non_highway_edges = None
        self.non_highway_nodes = None
        self.nodes = nodes
        self.edges = edges

    def remove_highways(self):
        if self.edges["highway"] is None:
            # generate error handling here
            return
        non_highway_edges = self.edges[
            (self.edges["highway"] != "primary") &
            (self.edges["highway"] != "motorway") &
            (self.edges["highway"] != "trunk") &
            (self.edges["highway"] != "primary_link") &
            (self.edges["highway"] != "motorway_link") &
            (self.edges["highway"] != "trunk_link")
        ]
        connected_nodes = pd.Index(non_highway_edges["u"].union(non_highway_edges["v"]))
        non_highway_nodes = self.nodes.loc[connected_nodes]
        self.non_highway_edges = non_highway_edges
        self.non_highway_nodes = non_highway_nodes

    # def clean_dataframe(dataframe: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
