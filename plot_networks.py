from utils_eaquilibrea_interface import convert_to_eaquilibrae_od_matrix
from utils_od_matrix_generator import generate_od_df
from utils_plotting import *
from utils_network_processing import *
import matplotlib.pyplot as plt

# edge_df, node_df = import_network("data/edges_small_grid_H.csv", "data/nodes_small_grid_2.csv")
# plot_network(edge_df, node_df, node_id_col='id',base_width=1, node_label=True, title="H network")


# fig, ax = plt.subplots(1,2, figsize=(20,10))
# plot_network(edge_df, node_df, node_id_col='id',
#                          node_label=True,
#                          color_col_num='green_overlap_percentage',
#                          base_width=1,
#                          legend=True,
#                          title=f"Network with green overlap percentage",cmap="Greens", ax=ax[0])
# plot_network(edge_df, node_df, node_id_col='id',
#                          node_label=True,
#                          color_col_num='slope',
#                          base_width=1,
#                          legend=True,
#                          title=f"Network with slope",cmap="coolwarm", ax=ax[1])

# plt.savefig("output/figures/network_H.png")
#
# size_od = max(node_df['id']) + 1
# od_df = generate_od_df(size_od, od_scenario="CORNER_2", max_demand=4000)
# plot_od_matrix(convert_to_eaquilibrae_od_matrix(od_df), edge_df, node_df)
# plt.savefig("output/figures/od_matrix.png")

test_name = "CAP_2_tunnel_corner_2_4000_bi2"
results_test_random_df = pd.read_csv(f"output/results_test_random_{test_name}.csv")

results_test_random_df["modal_share"].plot.kde(title=f"Modal Share Density for 10 bike lanes randomly selected \n ({test_name})")
plt.grid()
plt.xlabel("Modal Share (%)")
plt.axvline(x=8.4457, color='red', linestyle='--', linewidth=2, label=f'Mode share from Optimization : {8.2304}')
plt.show()