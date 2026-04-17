from utils_plotting import *
from utils_network_processing import *
import matplotlib.pyplot as plt
import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import LineString
from shapely import wkt
import pandas as pd
import requests

fig,ax = plt.subplots()
edge_df, node_df = import_network("data/Sioux_Falls/edges_Sioux_Falls.csv", "data/Sioux_Falls/nodes_Sioux_Falls.csv", real_network=True)
plot_network(edge_df, node_df, node_label=True, title="Sioux Falls Network", ax=ax)

# tags = { 'leisure': ['park','dog_park','pitch','garden','nature_reserve','marina'],
#                'landuse':['forest','meadow','grassland','farmland','farmyard','vineyard','orchard','farmland','recreation_ground','allotments','village_green','grass','greenfield','bassin'],
#                'grassland': True,
#                'natural': ['water','bay'],
#                 'surface': 'grass',
#                 'wetland' : True }
# gdf_park_SF = ox.features_from_place("Sioux Falls",tags)
# gdf_park_SF = gdf_park_SF[gdf_park_SF.geom_type.isin(['Polygon', 'MultiPolygon'])]
# gdf_park_SF = gdf_park_SF.to_crs(epsg=4326)
# gdf_park_SF.plot(ax=ax, color="green")
# plt.show()
#
# gdf_park_SF.to_csv("data/Sioux_Falls/green_Sioux_Falls.csv")

#
# def convert_df_to_gdf(edge_df, node_df):
#     edge_df['geometry'] = edge_df.apply(create_line, axis=1)
#     return gpd.GeoDataFrame(edge_df, geometry=edge_df.geometry)
#
# def create_line(row):
#     start_node = nodes_coords[row['a_node']]
#     end_node = nodes_coords[row['b_node']]
#
#     return LineString([(start_node['x'], start_node['y']),
#                        (end_node['x'], end_node['y'])])
#
# nodes_coords = node_df.set_index('id')[['x', 'y']].to_dict('index')
# edge_gdf = convert_df_to_gdf(edge_df, node_df)
# edge_gdf.set_crs(crs='epsg:4326', inplace=True)
#
# green_df_raw = pd.read_csv("data/Sioux_Falls/green_Sioux_Falls.csv")
# green_df_raw = green_df_raw['geometry'].apply(wkt.loads)
# green_gdf = gpd.GeoDataFrame(green_df_raw, geometry='geometry', crs="EPSG:4326")
# edge_gdf.to_crs("EPSG:3857", inplace=True)
# green_gdf.to_crs("EPSG:3857", inplace=True)
# green_gdf["green_area"] = green_gdf["geometry"].area
#
# buffer_gdf = gpd.GeoDataFrame(edge_gdf, geometry=edge_gdf.buffer(20))
# buffer_gdf["buffer_area"] = buffer_gdf["geometry"].area
#
# fig,ax = plt.subplots()
# edge_gdf.plot(ax=ax, color='black', linewidth=0.5)
# green_gdf.plot(ax=ax, color='green')
# buffer_gdf.plot(ax=ax, color='red', alpha=0.3)
# ax.set_xlim(-1.0765e7,-1.0770e7)
# ax.set_ylim(5.390e6,5.395e6)
# plt.show()
#
# fig,ax = plt.subplots()
# green_overlay_gdf = gpd.overlay(green_gdf, buffer_gdf, "intersection")
# green_overlay_gdf.plot(ax=ax)
# ax.set_xlim(-1.0765e7,-1.0770e7)
# ax.set_ylim(5.390e6,5.395e6)
# plt.show()
#
# green_overlay_gdf["green_overlay_area"] = green_overlay_gdf["geometry"].area
#
# other_cols = [c for c in green_overlay_gdf.columns if c not in ['id', 'geometry', 'green_overlay_area']]
# aggregation_logic = {col: 'first' for col in other_cols}
# aggregation_logic['green_overlay_area'] = 'sum'
#
# green_overlay_gdf = green_overlay_gdf.dissolve(by='id', aggfunc=aggregation_logic)
# green_overlay_gdf["green_overlap_percentage"] = (green_overlay_gdf["green_overlay_area"]/green_overlay_gdf["buffer_area"])*100
#
# columns_to_drop = [c for c in edge_df.columns]
# columns_to_drop = columns_to_drop[1:len(columns_to_drop)]
# green_overlay_gdf.drop(columns=columns_to_drop, inplace=True)
# edge_df = pd.merge(edge_df, green_overlay_gdf,how='left', left_on='id', right_on='id', suffixes=(None,None))
#
# fig, ax = plt.subplots(figsize=(5, 7.5))
# green_df_raw = pd.read_csv("data/Sioux_Falls/green_Sioux_Falls.csv")
# green_df_raw = green_df_raw['geometry'].apply(wkt.loads)
# green_gdf = gpd.GeoDataFrame(green_df_raw, geometry='geometry', crs="EPSG:4326")
#
# plot_network(edge_df, node_df, node_label=True, title="Sioux Falls Network", color_col_num="green_overlap_percentage", cmap="Greens", base_width=1, ax=ax)
# green_gdf.plot(ax=ax, color='green')
# ax.set_xlim(-96.8,-96.69)
# ax.set_ylim(43.477,43.617)
# plt.show()
#
# edge_df["speed_car"] = 20
# edge_df["speed_bike"] = 15
# edge_df["green_overlap_percentage"].fillna(0, inplace=True)
# edge_df.drop(columns=["free_flow_time_car","free_flow_time_bike","travel_time_car","travel_time_bike","nbr_car_lane","capacity_cars","capacity_bikes","alpha","beta","flow_car","flow_bike","length_bi","geometry","green_area","buffer_area","green_overlay_area","length"], inplace=True)
# edge_df.to_csv("data/Sioux_Falls/edges_Sioux_Falls_modif.csv")

#
# def get_elevation(lat, lon):
#     url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
#     response = requests.get(url).json()
#     return response['results'][0]['elevation']
#
# node_df['elevation'] = node_df.apply(lambda row: get_elevation(row['y'], row['x']), axis=1)
# node_df.to_csv("data/Sioux_Falls/nodes_Sioux_Falls_modif.csv")

# for row in edge_df.iterrows():
#     elevation_node_a = node_df[row['node_a']]['elevation']
#     elevation_node_b = node_df[row['node_b']]['elevation']
#     row["slope"]=((elevation_node_b-elevation_node_a)/row["length"])*100

edge_df['elev_a'] = edge_df['a_node'].map(node_df['elevation'])
edge_df['elev_b'] = edge_df['b_node'].map(node_df['elevation'])

edge_df['slope'] = ((edge_df['elev_b'] - edge_df['elev_a']) / edge_df['length']) * 100

edge_df.drop(columns=['elev_a', 'elev_b'], inplace=True)
edge_df["speed_car"] = 20
edge_df["speed_bike"] = 15
edge_df["slope"].fillna(0, inplace=True)
edge_df.drop(columns=["free_flow_time_car","free_flow_time_bike","travel_time_car","travel_time_bike","nbr_car_lane","capacity_cars","capacity_bikes","alpha","beta","flow_car","flow_bike","length_bi","length"], inplace=True)
edge_df.to_csv("data/Sioux_Falls/edges_Sioux_Falls_modif.csv")


print(edge_df.head())

fig, ax = plt.subplots(figsize=(5, 7.5))
plot_network(edge_df, node_df, node_label=True, title="Sioux Falls Network", color_col_num="slope", cmap="bwr", base_width=1, ax=ax)
ax.set_xlim(-96.8,-96.69)
ax.set_ylim(43.477,43.617)
plt.show()