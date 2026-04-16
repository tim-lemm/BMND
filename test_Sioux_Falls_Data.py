from utils_plotting import *
from utils_network_processing import *
import matplotlib.pyplot as plt
import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point


fig,ax = plt.subplots()
edge_df, node_df = import_network("data/Sioux_Falls/edges_Sioux_Falls.csv", "data/Sioux_Falls/nodes_Sioux_Falls.csv")
plot_network(edge_df, node_df, node_label=True, title="Sioux Falls Network", ax=ax)

tags = { 'leisure': ['park','dog_park','pitch','garden','nature_reserve','marina'],
               'landuse':['forest','meadow','grassland','farmland','farmyard','vineyard','orchard','farmland','recreation_ground','allotments','village_green','grass','greenfield','bassin'],
               'grassland': True,
               'natural': ['water','bay'],
                'surface': 'grass',
                'wetland' : True }
gdf_park_SF = ox.features_from_place("Sioux Falls",tags)
gdf_park_SF = gdf_park_SF[gdf_park_SF.geom_type.isin(['Polygon', 'MultiPolygon'])]
gdf_park_SF = gdf_park_SF.to_crs(epsg=4326)
gdf_park_SF.plot(ax=ax, color="green")
plt.show()

gdf_park_SF.to_csv("data/Sioux_Falls/green_Sioux_Falls.csv")