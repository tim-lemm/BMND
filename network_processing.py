import numpy as np
import pandas as pd


def calculate_length(node_df, edge_df):
    """ Calculate Euclidean length of edges based on node coordinates. """
    lengths = []
    for edge in edge_df.itertuples():
        a_node = node_df.loc[node_df['node'] == edge.a_node]
        b_node = node_df.loc[node_df['node'] == edge.b_node]
        length = np.sqrt((a_node['x'].values[0] - b_node['x'].values[0])**2 + (a_node['y'].values[0] - b_node['y'].values[0])**2)
        lengths.append(length)
    return edge_df.assign(length=lengths)

def calculate_length_bi(edge_df, weight = 0):
    if weight > 0.5 or weight < -0.2 :
        raise ValueError("Weight must be between 0.5 and -0.2")
    list_length_bi = []
    for row in edge_df.itertuples():
        if row.type_bike is None:
            if row.flow_car < 6000:
                list_length_bi.append(row.length * (0.8 - weight))
            elif row.flow_car >= 8000:
                list_length_bi.append(row.length * (1.4 + weight))
            elif 6000 <= row.flow_car < 7500:
                list_length_bi.append(row.length * 1)
            elif 7500 <= row.flow_car < 8000:
                list_length_bi.append(row.length * (1.2 + weight))
        else:
            list_length_bi.append(row.length * (0.5 - weight))
    edge_df["length_bi"] = list_length_bi
    return edge_df

def calculate_congested_time(edge_df, free_flow_time_name="free_flow_time", congested_time_name="congested_time", flow_name="flow", capacity_name="capacity", alpha=0.15, beta=4):
    """Calculate congested travel time using BPR function.
    𝑇=𝑇0(1+α(𝑉/𝐶)^β)
    where:
    - 𝑇 is the congested travel time
    - 𝑇0 is the free-flow travel time
    - 𝑉 is the volume (flow)
    - 𝐶 is the capacity
    - α and β are parameters
    """
    edge_df[congested_time_name]=edge_df[free_flow_time_name]*(1+alpha*(edge_df[flow_name]/edge_df[capacity_name])**beta)
    return edge_df

def update_network(edge_df, free_flow_time_name="free_flow_time_car", congested_time_name="congested_time", flow_name="flow", capacity_name="capacity", alpha=0.15, beta=4):
    edge_df = calculate_congested_time(edge_df, free_flow_time_name, congested_time_name, flow_name, capacity_name, alpha, beta)
    edge_df = calculate_length_bi(edge_df)
    edge_df["travel_time_bike"] = edge_df["length_bi"]/edge_df["speed_bike"]
    return edge_df

def import_network(edge_filepath:str, node_filepath:str, capacity_car:int = 3000):
    edge_df = pd.read_csv(edge_filepath)
    node_df = pd.read_csv(node_filepath)

    edge_df = calculate_length(node_df, edge_df)
    #edge_df["length"] *= 10
    edge_df["type_bike"] = None
    edge_df["speed_bike"] /= 3.6
    edge_df["speed_car"] /= 3.6
    edge_df["free_flow_time_car"] = edge_df["length"] / edge_df["speed_car"]
    edge_df["free_flow_time_bike"] = edge_df["length"] / edge_df["speed_bike"]
    edge_df["travel_time_car"] = edge_df["free_flow_time_car"]
    edge_df["travel_time_bike"] = edge_df["free_flow_time_bike"]
    edge_df["capacity_cars"] = capacity_car
    edge_df["capacity_bikes"] = 99999
    edge_df["alpha"] = 0.15
    edge_df["beta"] = 4
    edge_df["flow_car"] = 0
    edge_df["flow_bike"] = 0
    edge_df["length_bi"]= edge_df["length"]
    return edge_df, node_df

