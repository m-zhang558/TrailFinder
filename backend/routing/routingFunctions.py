import networkx as nx

def build_graph(nodes, edges):
    graph = nx.Graph()

    # add nodes
    for node in nodes.data:
        graph.add_node(
            node["id"],
            lat=node["lat"],
            lon=node["lon"],
        )

    # add edges
    for edge in edges.data:
        graph.add_edge(
            edge["u"],
            edge["v"],
            weight=edge["length"],
        )

    return graph

def get_route(start_id, end_id, graph):
    return nx.shortest_path(graph, start_id, end_id, weight="length")

