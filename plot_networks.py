
from utils_od_matrix_generator import *
from utils_plotting import *
from utils_network_processing import *
import geopandas as gpd

edge_df, node_df = import_network("data/edges_small_grid_2.csv", "data/nodes_small_grid_2.csv")

fig, ax = plt.subplots(1,2, figsize=(20,10))
plot_network(edge_df, node_df,
                         node_label=True,
                         color_col_num='green_overlap_percentage',
                         base_width=1,
                         legend=True,
                         title=f"Network with green overlap percentage",cmap="Greens", ax=ax[0])
plot_network(edge_df, node_df,
                         node_label=True,
                         color_col_num='slope',
                         base_width=1,
                         legend=True,
                         title=f"Network with slope",cmap="coolwarm", ax=ax[1])

plt.show()





edge_delft_df = pd.read_csv("data/Delft/edges.csv")
node_delft_df = pd.read_csv("data/Delft/nodes.csv")
edge_delft_df["type_bike"]="None"
plot_network(edge_delft_df, node_delft_df, node_id_col='id',
             color_col_str='type_bike',
                     base_width=0.1,
                     legend=True,
                     title=f"Network of Delft",
             node_size=10)
plt.show()

edge_delft_df = change_type_bike_infra_with_index(edge_delft_df, "bike_path",[1,2,3,4,5,6,7,8,9,10,11,12])

plot_network(edge_delft_df, node_delft_df, node_id_col='id',
             color_col_str='type_bike',
                     base_width=0.1,
                     legend=True,
                     title=f"Network of Delft",
             node_size=10)
plt.show()

# edge_delft_df["type_bike"] = "None"
# edge_delft_df["speed_car"] = edge_delft_df["speed"]
# edge_delft_df["speed_bike"] = 15
# edge_delft_df["length"] = edge_delft_df["length"]*1000
# edge_delft_df["free_flow_time"]=edge_delft_df["free_flow_time"]*3600
# edge_delft_df.drop(columns=["speed"], inplace=True)
# print(edge_delft_df.to_string())
# edge_delft_df.to_csv("data/Delft/edges.csv")
#
# od_gdf = gpd.read_file("data/Delft/od.gpkg")
# od_gdf.to_csv("data/Delft/od.csv", index=False)
# od_df = pd.read_csv("data/Delft/od.csv")
# od_df.drop(columns=["geometry"], inplace=True)
# od_df.to_csv("data/Delft/od.csv", index=False)

od_matrix = pd.read_csv("data/Delft/od.csv")
plot_od_matrix(od_matrix, edge_delft_df, node_delft_df, ax=None, figsize=(10, 10), title='OD Matrix',
                   label=False, color='red', vmax=None)
plt.show()