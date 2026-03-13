from utils_eaquilibrea_interface import convert_to_eaquilibrae_od_matrix
from utils_od_matrix_generator import generate_od_df
from utils_plotting import *
from utils_network_processing import *
import matplotlib.pyplot as plt

edge_df, node_df = import_network("data/edges_small_grid_2.csv", "data/nodes_small_grid_2.csv")

fig, ax = plt.subplots(1,2, figsize=(20,10))
plot_network(edge_df, node_df, node_id_col='id',
                         node_label=True,
                         color_col_num='green_overlap_percentage',
                         base_width=1,
                         legend=True,
                         title=f"Network with green overlap percentage",cmap="Greens", ax=ax[0])
plot_network(edge_df, node_df, node_id_col='id',
                         node_label=True,
                         color_col_num='slope',
                         base_width=1,
                         legend=True,
                         title=f"Network with slope",cmap="coolwarm", ax=ax[1])

plt.show()
size_od = max(node_df['id']) + 1
od_df = generate_od_df(size_od, od_scenario="CORNER", max_demand=2000)
plot_od_matrix(convert_to_eaquilibrae_od_matrix(od_df), edge_df, node_df)
plt.show()

results_test_random_df = pd.read_csv("output/results_test_random_df.csv")

results_test_random_df["modal_share"].plot.kde(title="Modal Share Density for 10 bike lanes randomly selected")
plt.grid()
plt.xlabel("Modal Share (%)")
plt.axvline(x=7.886975627149402, color='red', linestyle='--', linewidth=2, label=f'Mode share from Optimization : {7.886975627149402}')
plt.show()