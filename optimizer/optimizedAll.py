import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

from optimizer import aco as aco
from utils import roadLengthGraph as rlg

def optimize():
    # Create an empty graph
    CG = nx.DiGraph()

    # Load CSV file
    path = "the_amount_of_cars.csv"
    df = pd.read_csv(path)

    # Specify weights
    distWeight = 0.4
    trafficWeight = 0.6

    # Add nodes with labels
    CG.add_node(1, label="North Gate", pos=(0, 0))
    CG.add_node(2, label="President's Building Intersection", pos=(-3, 2))
    CG.add_node(3, label="Phai Lom Gate Intersection", pos=(-5, 5))
    CG.add_node(4, label="Tennis Court Roundabout", pos=(-3, 8))
    CG.add_node(5, label="ORMORCHOR Intersection", pos=(0, 8))
    CG.add_node(6, label="SCB Roundabout", pos=(-1, 3))
    CG.add_node(7, label="Humanities Roundabout", pos=(3, 5))
    CG.add_node(8, label="New Canteen Intersection", pos=(3, 8))
    CG.add_node(9, label="Ang Kaew Intersection", pos=(5, 3))
    CG.add_node(10, label="Tad Chomphu Pond Roundabout", pos=(5, 7))
    CG.add_node(11, label="Fai Hin Parking Lot", pos=(5, 11))
    CG.add_node(12, label="Clock Tower Roundabout", pos=(0, 11))
    CG.add_node(13, label="Faculty of Engineering", pos=(0, 13))


    # Loop over each day to create intervals from 6 AM to 6 PM
    write_csv = []
    for index, row in df.iterrows():
        edges = [
            (1, 2, df['Edge 1'][index]),
            (1, 9, df['Edge 2'][index]),
            (2, 3, df['Edge 3'][index]),
            (2, 6, df['Edge 4'][index]),
            (6, 7, df['Edge 5'][index]),
            (7, 9, df['Edge 6'][index]),
            (9, 10, df['Edge 7'][index]),
            (3, 4, df['Edge 8'][index]),
            (6, 5, df['Edge 9'][index]),
            (7, 5, df['Edge 10'][index]),
            (7, 8, df['Edge 11'][index]),
            (7, 10, df['Edge 12'][index]),
            (10, 11, df['Edge 13'][index]),
            (4, 5, df['Edge 14'][index]),
            (5, 8, df['Edge 15'][index]),
            (11, 8, df['Edge 16'][index]),
            (5, 12, df['Edge 17'][index]),
            (8 ,12, df['Edge 18'][index]),
            (12, 13, df['Edge 19'][index])
        ]
        for start, end, distance in edges:
            CG.add_edge(start, end, weight=distance)

        # call aco
        try:
            aco_path, aco_cost = aco.aco2(rlg.initGraph(), CG, distWeight, trafficWeight)
            node_path = []
            for node in aco_path:
                node_path.append(CG.nodes[node]['label'])
        except Exception:
            # debug
            print(f"{df['Time Interval'][index]}: No path found")
            write_csv.append([df['Time Interval'][index], 'No path found', aco_cost])
        else:
            # debug
            print(f"{df['Time Interval'][index]}: [{' -> '.join(map(str, node_path))}]")
            write_csv.append([df['Time Interval'][index], ' -> '.join(map(str, node_path)), aco_cost])
    
    # Convert the result list into a DataFrame
    columns = ['Time Interval', 'Optimal Path', 'Cost']
    df_result = pd.DataFrame(write_csv, columns=columns)

    # Save the results to a CSV file
    output_path = 'optimal_solution_all.csv'
    df_result.to_csv(output_path, index=False)

    print(f"Results saved to {output_path}")

        

