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
    path_node_id = nx.shortest_path(graph, start_id, end_id, weight="weight")
    path_coordinates = []
    for node in path_node_id:
        path_coordinates.append([graph.nodes[node]["lat"], graph.nodes[node]["lon"]])
    return path_coordinates

