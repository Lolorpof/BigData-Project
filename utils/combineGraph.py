# combineGraph.py
import networkx as nx

def combine(distGraph: nx.Graph, trafficGraph: nx.Graph, distWeight: float, trafficWeight: float):
    # Init var
    minVal = 0.1
    maxVal = 1
    newGraph = nx.Graph()
    # distance setup
    normDistEdges = {}
    dist_weights = [d['weight'] for u, v, d in distGraph.edges(data=True)]
    minDist = min(dist_weights)
    maxDist = max(dist_weights)

    # traffic setup
    normTrafficEdges = {}
    traffic_weights = [d['weight'] for u, v, d in trafficGraph.edges(data=True)]
    minTraffic = min(traffic_weights)
    maxTraffic = max(traffic_weights)

    # normalize to [0,1]
    # set up normalize edges in distGraph
    for edge in distGraph.edges:
        weight = distGraph.get_edge_data(edge[0], edge[1]).get("weight")
        # normalize the weight
        normDistEdges[edge] = minVal + (((weight - minDist) / (maxDist - minDist)) * (maxVal - minVal))
    # set up normalize edges in trafficGraph
    for edge in trafficGraph.edges:
        weight = trafficGraph.get_edge_data(edge[0], edge[1]).get("weight")
        # normalize the weight
        normTrafficEdges[edge] = minVal + (((weight - minTraffic) / (maxTraffic - minTraffic)) * (maxVal - minVal))

    # combine normalize edges from 2 graphs (if it is แยกอมช(5) then the cost is 1(worst))
    normEdges = {}
    for edge in distGraph.edges:
        normEdges[edge] = distWeight * normDistEdges[edge]
        + trafficWeight * normTrafficEdges[edge] if ((edge[0] != 5 and edge[1] != 5)
                                                     or ((edge[0] == 5 and edge[1] == 12)
                                                        or (edge[0] == 12 and edge[1] == 5))
                                                     ) else 1

    # add nodes to newGraph with attributes
    for node in distGraph.nodes:
        newGraph.add_node(node, **distGraph.nodes[node])

    # add edges to newGraph with attributes
    for edge in distGraph.edges:
        newGraph.add_edge(edge[0], edge[1], cost=normEdges[edge])

    return newGraph

# testing
# g = nx.Graph()
# g.add_nodes_from([(1, {"label": "duangjun", "pos": (0,0)}), (2, {"label": "borwon", "pos": (2,1)})])
# g.add_weighted_edges_from([(1, 2, 5)])

# print(g.is_directed())
# for node in g.nodes:
#     print(g.nodes[node]["pos"])

# for edge in g.edges:
#     print(g.get_edge_data(edge[0], edge[1]).get("weight"))