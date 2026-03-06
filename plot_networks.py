from utils_plotting import *
from utils_network_processing import *

edge_df, node_df = import_network("data/edges_small_grid_2.csv", "data/nodes_small_grid_2.csv")

fig, ax = plt.subplots(1,2, figsize=(20,10))
plot_network(edge_df, node_df, node_id_col='node',
                         node_label=True,
                         color_col_num='green_overlap_percentage',
                         base_width=1,
                         legend=True,
                         title=f"Network with green overlap percentage",cmap="Greens", ax=ax[0])
plot_network(edge_df, node_df, node_id_col='node',
                         node_label=True,
                         color_col_num='slope',
                         base_width=1,
                         legend=True,
                         title=f"Network with slope",cmap="coolwarm", ax=ax[1])

plt.show()