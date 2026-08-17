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
from pyproj import Transformer
plt.rcParams.update({'font.size': 10})

city_name = "Delft"

# node_df = pd.read_csv(
#     f"data/{city_name}/nodes_{city_name}.csv" )
#
# print(node_df.head())
#
# transformer = Transformer.from_crs("EPSG:2154", "EPSG:4326", always_xy=True)
#
# node_df['lon'], node_df['lat'] = transformer.transform(
#     node_df['x'].values,
#     node_df['y'].values
# )
# print(node_df.head())
# node_df.drop(columns=['x', 'y'], inplace=True)
#
# node_df = node_df.rename(columns={"lon": "x", "lat": "y"})
# node_df.to_csv(
#     f"data/{city_name}/nodes_{city_name}.csv"
# )

fig,ax = plt.subplots()
edge_df, node_df = import_network(f"data/{city_name}/edges_{city_name}.csv", f"data/{city_name}/nodes_{city_name}.csv", real_network=True, keep_length=True)
plot_network(edge_df, node_df, node_label=True, title=f"{city_name} Network", ax=ax, base_width=0.3, show_nodes=False)
plt.show()


# tags = { 'leisure': ['park','dog_park','pitch','garden','nature_reserve','marina'],
#                'landuse':['forest','meadow','grassland','farmland','farmyard','vineyard','orchard','farmland','recreation_ground','allotments','village_green','grass','greenfield','bassin'],
#                'grassland': True,
#                'natural': ['water','bay'],
#                 'surface': 'grass',
#                 'wetland' : True }
# gdf_park = ox.features_from_place(f"{city_name}",tags)
# gdf_park = gdf_park[gdf_park.geom_type.isin(['Polygon', 'MultiPolygon'])]
# gdf_park = gdf_park.to_crs(epsg=4326)

# df_park = pd.read_csv(f"data/{city_name}/green_{city_name}.csv")
# gdf_park = gpd.GeoDataFrame(
#     df_park, geometry=gpd.GeoSeries.from_wkt(df_park["geometry"]), crs="EPSG:4326"
# )
# gdf_park.plot(color="green")
# plt.show()

# gdf_park.to_csv(f"data/{city_name}/green_{city_name}.csv")

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

# nodes_coords = node_df.set_index('id')[['x', 'y']].to_dict('index')
# edge_gdf = convert_df_to_gdf(edge_df, node_df)
# edge_gdf.set_crs(crs='epsg:4326', inplace=True)
# edge_gdf.explore().save("ma_carte.html")
# edge_gdf = gpd.read_file(f"data/{city_name}/links.gpkg")
# edge_gdf = edge_gdf.to_crs("EPSG:4326")
# edge_gdf.explore().save(f"data/{city_name}/{city_name}_carte.html")


# green_df_raw = pd.read_csv(f"data/{city_name}/green_{city_name}.csv")
# green_df_raw = green_df_raw['geometry'].apply(wkt.loads)
# green_gdf = gpd.GeoDataFrame(green_df_raw, geometry='geometry', crs="EPSG:4326")
# # green_gdf.explore().save(f"data/{city_name}/{city_name}_carte_green.html")
#
# edge_gdf.to_crs("EPSG:3857", inplace=True)
# green_gdf.to_crs("EPSG:3857", inplace=True)
# green_gdf["green_area"] = green_gdf["geometry"].area
#
# buffer_gdf = gpd.GeoDataFrame(edge_gdf, geometry=edge_gdf.buffer(20))
# buffer_gdf["buffer_area"] = buffer_gdf["geometry"].area
#
# fig,ax = plt.subplots()
#
# plot_limites_xmax = 487500
# plot_limites_xmin = 485000
# plot_limites_ymax = 6.800e6
# plot_limites_ymin = 6.801e6
#
# edge_gdf.plot(ax=ax, color='black', linewidth=0.5)
# green_gdf.plot(ax=ax, color='green')
# buffer_gdf.plot(ax=ax, color='red', alpha=0.3)
# ax.set_xlim(plot_limites_xmin,plot_limites_xmax)
# ax.set_ylim(plot_limites_ymin,plot_limites_ymax)
# plt.show()
#
# fig,ax = plt.subplots()
# green_overlay_gdf = gpd.overlay(green_gdf, buffer_gdf, "intersection")
# green_overlay_gdf.plot(ax=ax)
# ax.set_xlim(plot_limites_xmin,plot_limites_xmax)
# ax.set_ylim(plot_limites_ymin,plot_limites_ymax)
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
# edge_df = pd.merge(edge_df, green_overlay_gdf['green_overlap_percentage'], how='left', left_on='id', right_on='id', suffixes=(None,None))
# edge_df['green_overlap_percentage'] = edge_df['green_overlap_percentage'].clip(upper=100)
# edge_df['green_overlap_percentage'] = edge_df['green_overlap_percentage'].fillna(0)
#
# plot_network(edge_df, node_df, node_label=True, title=f"{city_name} Network - green_overlap_percentage", color_col_num="green_overlap_percentage", base_width=0.3, show_nodes=False, cmap="Greens")
# plt.show()
#
# edge_df.to_csv(f"data/{city_name}/edges_{city_name}_real.csv")



# def get_elevation(lat, lon):
#     url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
#     response = requests.get(url).json()
#     return response['results'][0]['elevation']
#
# node_df['elevation'] = node_df.apply(lambda row: get_elevation(row['y'], row['x']), axis=1)
# node_df.to_csv(f"data/{city_name}/nodes_{city_name}_modif.csv")

#
# for index, row in edge_df.iterrows():
#     id_a = row['a_node']
#     elevation_node_a = node_df[node_df['id'] == id_a]['elevation'].values[0]
#     id_b = row['b_node']
#     elevation_node_b = node_df[node_df['id'] == id_b]['elevation'].values[0]
#     row["slope"]=((elevation_node_b-elevation_node_a)/row["length"])*100
#
# edge_df['elev_a'] = edge_df['a_node'].map(node_df['elevation'])
# edge_df['elev_b'] = edge_df['b_node'].map(node_df['elevation'])
#
# edge_df['slope'] = ((edge_df['elev_b'] - edge_df['elev_a']) / edge_df['length']) * 100
#
# edge_df.drop(columns=['elev_a', 'elev_b'], inplace=True)
# edge_df["slope"].fillna(0, inplace=True)
# # edge_df.drop(columns=["free_flow_time_car","free_flow_time_bike","travel_time_car","travel_time_bike","nbr_car_lane","capacity_cars","capacity_bikes","alpha","beta","flow_car","flow_bike","length_bi","length"], inplace=True)
# edge_df.to_csv(f"data/{city_name}/edges_{city_name}.csv", index=False)

fig, ax = plt.subplots(figsize=(5, 7.5))
plot_network(edge_df, node_df, node_label=True, title=f"{city_name} Network (slope)", color_col_num="slope", cmap="bwr", base_width=0.3, show_nodes=False, ax=ax)
plt.show()

fig, ax = plt.subplots(figsize=(5, 7.5))
plot_network(edge_df, node_df, node_label=True, title=f"{city_name} Network (number of car lanes)", ax=ax, color_col_num="init_nbr_car_lane", base_width=0.3, cmap="summer_r", show_nodes=False)
plt.show()

fig, ax = plt.subplots(figsize=(5, 7.5))
plot_network(edge_df, node_df, node_label=True, title=f"{city_name} Network (capacity)", ax=ax, color_col_num="capacity", base_width=0.3, cmap="summer_r", show_nodes=False)
plt.show()

fig, ax = plt.subplots(figsize=(5, 7.5))
plot_network(edge_df, node_df, node_label=True, title=f"{city_name} Network (Bike infrastructure)", ax=ax, color_col_str="type_bike", base_width=0.3, show_nodes=False, legend=True)
plt.show()