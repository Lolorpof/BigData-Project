import networkx as nx
import pandas as pd
from datetime import datetime, timedelta

from optimizer import aco as aco
from utils import roadLengthGraph as rlg

def optimize():
    # Create an empty graph
    CG = nx.Graph()

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

    # Get specific time and range
    # datetime now depends on system?
    # currentTime = datetime.now() 
    currentTime = datetime.now() + timedelta(hours=10)

    currentMin = currentTime.minute
    start_hour = currentTime.hour
    start_min = currentMin - (currentMin % 10) if (currentMin % 10) <= 5 else currentMin - ((currentMin % 10) - 5)
    end_hour = currentTime.hour if currentMin <= 55 else currentTime.hour + 1
    end_min = currentMin + (5 - (currentMin % 10)) if (currentMin % 10) <= 5 else (currentMin + (10 - (currentMin % 10)) if currentMin <= 55 else 0)

    start_time = currentTime.replace(hour=start_hour, minute=start_min, second=0, microsecond=0)
    end_time = currentTime.replace(hour=end_hour, minute=end_min, second=0, microsecond=0)

    # for debugging
    ct = currentTime.time().strftime("%H:%M:%S")
    print(f"Current Time: {ct}")
    # print(start_time.time())
    # print(end_time.time())

    # Loop to get the current time period
    st =start_time.time().strftime("%H:%M:%S")
    et = end_time.time().strftime("%H:%M:%S")
    currentInd = -1
    for index, row in df.iterrows():
        timePeriod = df['Time Interval'][index]
        if st in timePeriod and et in timePeriod:
            currentInd = index
            break

    if (currentInd == -1):
        print("No data available for this time period")
        return
    
    # Set edges cost
    edges = [
            (1, 2, df['Edge 1'][currentInd]),
            (1, 9, df['Edge 2'][currentInd]),
            (2, 3, df['Edge 3'][currentInd]),
            (2, 6, df['Edge 4'][currentInd]),
            (6, 7, df['Edge 5'][currentInd]),
            (7, 9, df['Edge 6'][currentInd]),
            (9, 10, df['Edge 7'][currentInd]),
            (3, 4, df['Edge 8'][currentInd]),
            (6, 5, df['Edge 9'][currentInd]),
            (7, 5, df['Edge 10'][currentInd]),
            (7, 8, df['Edge 11'][currentInd]),
            (7, 10, df['Edge 12'][currentInd]),
            (10, 11, df['Edge 13'][currentInd]),
            (4, 5, df['Edge 14'][currentInd]),
            (5, 8, df['Edge 15'][currentInd]),
            (11, 8, df['Edge 16'][currentInd]),
            (5, 12, df['Edge 17'][currentInd]),
            (8 ,12, df['Edge 18'][currentInd]),
            (12, 13, df['Edge 19'][currentInd])
        ]
    for start, end, distance in edges:
        CG.add_edge(start, end, weight=distance)

    # call aco
    write_csv = []
    try:
        aco_path, aco_cost = aco.aco2(rlg.initGraph(), CG, distWeight, trafficWeight)
        node_path = []
        for node in aco_path:
            node_path.append(CG.nodes[node]['label'])
    except Exception:
        # debug
        # print(f"{df['Time Interval'][currentInd]}: No path found")
        write_csv.append([df['Time Interval'][currentInd], 'No path found', aco_cost])
    else:
        # debug
        # print(f"{df['Time Interval'][currentInd]}: [{' -> '.join(map(str, node_path))}]")
        write_csv.append([df['Time Interval'][currentInd], ' -> '.join(map(str, node_path)), aco_cost])

    # Convert the result list into a DataFrame
    columns = ['Time Interval', 'Optimal Path', 'Cost']
    df_result = pd.DataFrame(write_csv, columns=columns)

    # Save the results to a CSV file
    output_path = 'optimal_solution_current.csv'
    df_result.to_csv(output_path, index=False)

    print(f"Results saved to {output_path}")

