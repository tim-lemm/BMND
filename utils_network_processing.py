import numpy as np
import pandas as pd
from utils_od_matrix_generator import *
from geopy.distance import geodesic

def calculate_length(node_df, edge_df):
    """ Calculate Euclidean length of edges based on node coordinates. """
    lengths = []
    for edge in edge_df.itertuples():
        a_node = node_df.loc[node_df['id'] == edge.a_node]
        b_node = node_df.loc[node_df['id'] == edge.b_node]
        length = np.sqrt((a_node['x'].values[0] - b_node['x'].values[0])**2 + (a_node['y'].values[0] - b_node['y'].values[0])**2)
        lengths.append(length)
    return edge_df.assign(length=lengths)

def calculate_length_real(node_df, edge_df):
    def get_coords(node_id):
        node_row = node_df[node_df['id'] == node_id]
        if not node_row.empty:
            return (node_row['y'].values[0], node_row['x'].values[0])
        else:
            raise KeyError(f"Nœud {node_id} non trouvé dans la colonne 'id'")

    edge_df['length'] = edge_df.apply(
        lambda row: geodesic(
            get_coords(row["a_node"]),
            get_coords(row["b_node"])
        ).meters,
        axis=1
    )
    return edge_df

def calculate_length_bi(edge_df, weight = 0):
    if weight > 0.5 or weight < -0.2 :
        raise ValueError("Weight must be between 0.5 and -0.2")
    list_length_bi = []
    for row in edge_df.itertuples():
        if row.type_bike == "None":
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

def slope_coef(value, slope):
    if slope <= -2.5:
        return value - 0.1
    elif slope >= 2.5:
        return value + 0.1
    else:
        return value

def calculate_length_bi_2(edge_df, bias = 0, weight=1):
    list_length_bi = []
    for row in edge_df.itertuples():
        if row.type_bike == "None":
            if row.flow_car < weight*(6000+bias):
                list_length_bi.append(row.length * slope_coef(0.8, row.slope))
            elif row.flow_car >= weight*(8000+bias):
                list_length_bi.append(row.length * slope_coef(1.4, row.slope))
            elif weight*(6000+bias) <= row.flow_car < weight*(7500+bias):
                list_length_bi.append(row.length * slope_coef(1, row.slope))
            elif weight*(7500+bias) <= row.flow_car < weight*(8000+bias):
                list_length_bi.append(row.length * slope_coef(1.2, row.slope))
        else:
            if row.green_overlap_percentage > 51:
                list_length_bi.append(row.length * slope_coef(0.2, row.slope))
            else:
                list_length_bi.append(row.length * slope_coef(0.4, row.slope))
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

def update_car_capacity(edge_df:pd.DataFrame, capacity_car:int = 1500):
    edge_df.loc[edge_df["type_bike"] == "bike_path", "nbr_car_lane"] = edge_df.loc[edge_df["type_bike"] == "bike_path", "init_nbr_car_lane"] - 1
    edge_df.loc[edge_df["type_bike"] == "None", "nbr_car_lane"] = edge_df.loc[edge_df["type_bike"] == "None", "init_nbr_car_lane"]
    edge_df["capacity_cars"] = edge_df["nbr_car_lane"] * capacity_car
    return edge_df

def update_network(edge_df, free_flow_time_name="free_flow_time_car", congested_time_name="congested_time", flow_name="flow", capacity_name="capacity", alpha=0.15, beta=4, CAP = True):
    edge_df = calculate_congested_time(edge_df, free_flow_time_name, congested_time_name, flow_name, capacity_name, alpha, beta)
    edge_df = calculate_length_bi_2(edge_df, bias=5000, weight=1)
    if CAP:
        edge_df = update_car_capacity(edge_df)
    edge_df["travel_time_bike"] = edge_df["length_bi"]/edge_df["speed_bike"]
    return edge_df

def import_network(edge_filepath:str, node_filepath:str, capacity_car:int = 1500, real_network=False):
    edge_df = pd.read_csv(edge_filepath)
    node_df = pd.read_csv(node_filepath)

    if real_network:
        edge_df = calculate_length_real(node_df, edge_df)
        edge_df['nbr_car_lane'] = edge_df['init_nbr_car_lane']
    else :
        edge_df = calculate_length(node_df, edge_df)
        edge_df["nbr_car_lane"] = 2

    edge_df["capacity_cars"] = edge_df["nbr_car_lane"] * capacity_car
    #edge_df["length"] *= 10
    edge_df["type_bike"] = "None"
    edge_df["speed_bike"] /= 3.6
    edge_df["speed_car"] /= 3.6
    edge_df["free_flow_time_car"] = edge_df["length"] / edge_df["speed_car"]
    edge_df["free_flow_time_bike"] = edge_df["length"] / edge_df["speed_bike"]
    edge_df["travel_time_car"] = edge_df["free_flow_time_car"]
    edge_df["travel_time_bike"] = edge_df["free_flow_time_bike"]

    edge_df["capacity_bikes"] = 99999
    edge_df["alpha"] = 0.15
    edge_df["beta"] = 4
    edge_df["flow_car"] = 0
    edge_df["flow_bike"] = 0
    edge_df["length_bi"]= edge_df["length"]
    return edge_df, node_df


def load_test_scenario(name_test_scenario:str, od_scenario:str, demand:int = 4000):
    edge_file_path = f"data/edges_{name_test_scenario}.csv"
    node_file_path = f"data/nodes_{name_test_scenario}.csv"
    edge_df, node_df = import_network(edge_file_path, node_file_path)

    size_od = max(node_df['id']) + 1
    od_df = generate_od_df(size_od, od_scenario=od_scenario, max_demand=demand)
    return edge_df, node_df, od_df

def change_type_bike_infra(edge_df:pd.DataFrame, new_type_bike:str, a_node:int, b_node:int):
    mask = (edge_df["a_node"] == a_node) & (edge_df["b_node"] == b_node)
    edge_df.loc[mask, "type_bike"] = new_type_bike
    return edge_df

def change_type_bike_infra_with_index(edge_df:pd.DataFrame, new_type_bike:str, index):
    if type(index) == int:
        index = [index]
    edge_df.loc[edge_df['id'].isin(index), "type_bike"] = new_type_bike
    return edge_df

def change_type_bike_infra_loop(edge_df:pd.DataFrame, new_type_bike:str,list_node:list):
    for a_node in list_node:
        for b_node in list_node:
            edge_df = change_type_bike_infra(edge_df, new_type_bike, a_node, b_node)
    return edge_df

def apply_bike_infra_scenario(edge_df:pd.DataFrame, num_scenario:int):
    list_node = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    edge_df = change_type_bike_infra_loop(edge_df, "None", list_node)
    if num_scenario == 0:
        return edge_df
    if num_scenario == 1:
        list_node = [1, 2, 3, 4, 5, 9, 13, 14, 15, 16, 12, 8]
        change_type_bike_infra_loop(edge_df, "bike_path",list_node)
        return edge_df
    if num_scenario == 2:
        edge_df["type_bike"] = "bike_path"
        return edge_df
    if num_scenario == 3:
        list_road = [[2, 6, 10, 14],[3,7,11,15],[5,6,7,8],[9,10,11,12]]
        for road in list_road:
            edge_df = change_type_bike_infra_loop(edge_df, "bike_path", road)
        return edge_df
    if num_scenario == 4:
        list_road = [[2, 6, 10, 14], [9,10,11,12]]
        for road in list_road:
            edge_df = change_type_bike_infra_loop(edge_df, "bike_path", road)
        return edge_df
    if num_scenario == 5:
        list_road = [[1, 2, 6, 7, 11, 12, 16], [4, 3, 7, 6,10,9,13]]
        for road in list_road:
            edge_df = change_type_bike_infra_loop(edge_df, "bike_path", road)
        return edge_df
    else:
        raise ValueError("Pleas choose a valid scenario (0 to 5)")