from utils_eaquilibrea_interface import convert_to_eaquilibrae_od_matrix
from utils_od_matrix_generator import generate_od_df
from utils_plotting import *
from utils_network_processing import *
import matplotlib.pyplot as plt

list_test_name = ["grid","H","tunnel","tunnel_ng"]
for test_name in list_test_name:
    edge_df, node_df = import_network(f"data/edges_{test_name}.csv", f"data/nodes_{test_name}.csv")
    plot_network(edge_df, node_df, node_id_col='id',base_width=1, node_label=True, title=f"{test_name} network")
    plt.savefig(f"output/_hEART_article/figures/_networks/{test_name}_simple_network.png")
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

    plt.savefig(f"output/_hEART_article/figures/_networks/{test_name}_networks.png")

list_test_name = ["grid","H","tunnel"]
fig, ax = plt.subplots(1,3, figsize=(30,10))
for i, test_name in enumerate(list_test_name):
    edge_df, node_df = import_network(f"data/edges_{test_name}.csv", f"data/nodes_{test_name}.csv")
    plot_network(edge_df, node_df, node_id_col='id',base_width=1, node_label=True, title=test_name, ax=ax[i])
plt.savefig(f"output/_hEART_article/figures/_networks/_all_simple_network.png")

# size_od = max(node_df['id']) + 1
# od_df = generate_od_df(size_od, od_scenario="CORNER_2", max_demand=4000)
# plot_od_matrix(convert_to_eaquilibrae_od_matrix(od_df), edge_df, node_df)
# plt.savefig("output/figures/od_matrix.png")