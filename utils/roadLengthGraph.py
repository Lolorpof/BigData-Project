import networkx as nx
import matplotlib.pyplot as plt

def initGraph():
    # Create an empty graph
    G = nx.Graph()

    # Add nodes with labels
    G.add_node(1, label="North Gate", pos=(0, 0))
    G.add_node(2, label="President's Building Intersection", pos=(-3, 2))
    G.add_node(3, label="Phai Lom Gate Intersection", pos=(-5, 5))
    G.add_node(4, label="Tennis Court Roundabout", pos=(-3, 8))
    G.add_node(5, label="ORMORCHOR Intersection", pos=(0, 8))
    G.add_node(6, label="SCB Roundabout", pos=(-1, 3))
    G.add_node(7, label="Humanities Roundabout", pos=(3, 5))
    G.add_node(8, label="New Canteen Intersection", pos=(3, 8))
    G.add_node(9, label="Ang Kaew Intersection", pos=(5, 3))
    G.add_node(10, label="Tad Chomphu Pond Roundabout", pos=(5, 7))
    G.add_node(11, label="Fai Hin Parking Lot", pos=(5, 11))
    G.add_node(12, label="Clock Tower Roundabout", pos=(0, 11))
    G.add_node(13, label="Faculty of Engineering", pos=(0, 13))

    # Define Edges with Distances and Directions
    edges = [
        (1, 2, 447),
        (1, 9, 706),
        (2, 3, 666),
        (2, 6, 170),
        (6, 7, 370),
        (7, 9, 437),
        (9, 10, 233),
        (3, 4, 270),
        (6, 5, 606),
        (7, 5, 523),
        (7, 8, 466),
        (7, 10, 318),
        (10, 11, 493),
        (4, 5, 233),
        (5, 8, 150),
        (11, 8, 358),
        (5, 12, 319),
        (8 ,12, 452),
        (12, 13, 340)
    ]

    for start, end, distance in edges:
        G.add_edge(start, end, weight=distance)

    return G

# # Draw the Graph with Directions
# plt.figure(figsize=(30, 30))

# # Specify positions manually
# pos = nx.get_node_attributes(G, 'pos')
# labels = nx.get_node_attributes(G, 'label')

# # Draw nodes and edges with arrows to indicate direction
# nx.draw(G, pos, labels=labels, with_labels=True, node_size=2000, node_color="skyblue",
#         font_size=5, edge_color="gray", arrows=True, connectionstyle="arc3,rad=0.1")

# # Add edge labels for distance and direction
# edge_labels = {(u, v): f"{d['weight']} m" for u, v, d in G.edges(data=True)}
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=5, label_pos=0.5)

# plt.title("Graph with Directional Edges and Labels (ภาษาไทย)")
# plt.axis('equal')
# plt.show()