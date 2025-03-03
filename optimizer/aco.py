# ACO initialization
import acopy as a1
import networkx as nx
import aco_routing as a2

from utils import combineGraph as cG

start_node = 1
end_node = 13

# not used
def aco1(distGraph: nx.Graph, trafficGraph: nx.Graph, distWeight: float, trafficWeight: float):
    # variables
    number_of_ants = 100
    iterations = 100
    alpha = 1.5
    beta = 1
    rho = 0.4
    pheremone_per_ant = 1

    solver = a1.Solver(rho=rho, q=pheremone_per_ant)
    colony = a1.Colony(alpha=alpha, beta=beta)

    traffic_graph = cG.combine(distGraph=distGraph, trafficGraph=trafficGraph,
                               distWeight=distWeight, trafficWeight=trafficWeight)

    return solver.optimize(graph=traffic_graph, colony=colony, limit=iterations, gen_size=number_of_ants)

def aco2(distGraph: nx.DiGraph, trafficGraph: nx.DiGraph, distWeight: float, trafficWeight: float):
    # variables
    number_of_ants = 100
    iterations = 100
    alpha = 1
    beta = 1.5
    rho = 0.1

    traffic_graph = cG.combine(distGraph=distGraph, trafficGraph=trafficGraph,
                               distWeight=distWeight, trafficWeight=trafficWeight)

    # print(traffic_graph.edges(data=True))
                            
    x = a2.ACO(graph=traffic_graph, evaporation_rate=rho, alpha=alpha, beta=beta, num_iterations=iterations, ant_max_steps=100,ant_random_spawn=False)

    return x.find_shortest_path(source=start_node, destination=end_node, num_ants=number_of_ants)
