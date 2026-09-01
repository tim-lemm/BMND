from utils_eaquilibrea_interface import convert_to_eaquilibrae_od_matrix
from utils_od_matrix_generator import generate_od_df
from utils_plotting import *
from utils_network_processing import *
import matplotlib.pyplot as plt
import glob
from PIL import Image
import os
import re
plt.rcParams.update({'font.size': 30})




# list_test_name = ["grid","H","tunnel","tunnel_ng"]
# for test_name in list_test_name:
#     edge_df, node_df = import_network(f"data/edges_{test_name}.csv", f"data/nodes_{test_name}.csv")
#     plot_network(edge_df, node_df, node_id_col='id',base_width=1, node_label=True, title=f"{test_name} network")
#     plt.savefig(f"output/_hEART_article/figures/_networks/{test_name}_simple_network.png")
#     fig, ax = plt.subplots(1,2, figsize=(20,10))
#     plot_network(edge_df, node_df, node_id_col='id',
#                              node_label=True,
#                              color_col_num='green_overlap_percentage',
#                              base_width=1,
#                              legend=True,
#                              title=f"Network with green overlap percentage",cmap="Greens", ax=ax[0])
#     plot_network(edge_df, node_df, node_id_col='id',
#                              node_label=True,
#                              color_col_num='slope',
#                              base_width=1,
#                              legend=True,
#                              title=f"Network with slope",cmap="coolwarm", ax=ax[1])
#
#     plt.savefig(f"output/_hEART_article/figures/_networks/{test_name}_networks.png")

# list_test_name = ["grid","H","tunnel"]
# fig, ax = plt.subplots(3,1, figsize=(15,30))
# for i, test_name in enumerate(list_test_name):
#     edge_df, node_df = import_network(f"data/edges_{test_name}.csv", f"data/nodes_{test_name}.csv")
#     plot_network(edge_df, node_df, node_id_col='id',base_width=1, node_label=True, title=test_name, ax=ax[i])
# ax[0].set_title("Grid Network\n (scenario A)")
# ax[1].set_title("H Network\n (scenario B)")
# ax[2].set_title("Tunnel Network\n (scenario C and D)")
# plt.tight_layout()
# plt.savefig(f"output/_hEART_article/figures/_networks/_all_simple_network.png")
# plt.show()

# fig, ax = plt.subplots(figsize=(15,15))
# size_od = max(node_df['id']) + 1
# od_df = generate_od_df(size_od, od_scenario="CORNER_2", max_demand=4000)
# plot_od_matrix(convert_to_eaquilibrae_od_matrix(od_df), edge_df, node_df, ax=ax)
# plt.savefig("output/figures/od_matrix.png")
# plt.show()
# edge_df, node_df = import_network(f"data/edges_tunnel.csv", f"data/nodes_tunnel.csv")
# plot_network(edge_df, node_df, node_id_col='id',base_width=1, node_label=True, title=f"Test network (tunnel) with topology and green spaces", figsize= (10,10))
# plt.savefig(f"output/_hEART_article/figures/_networks/empty_simple_network_tunnel.png", transparent=True)

# fig, ax = plt.subplots(2,1, figsize=(15,30))
# edge_df, node_df = import_network("data/edges_grid.csv", "data/nodes_grid.csv")
# plot_network(edge_df, node_df, node_id_col='id',base_width=1, node_label=True, title="Green overlap percentage", ax=ax[0], color_col_num="green_overlap_percentage", cmap="Greens")
# plot_network(edge_df, node_df, node_id_col='id',base_width=1, node_label=True, title="Slope (%)", ax=ax[1], color_col_num="slope", cmap="bwr")
# plt.tight_layout()
# plt.savefig("output/_hEART_article/figures/_networks/grid_networks.png")

## Plot of different maps

city_name = "Sioux_Falls"

edge_df, node_df = import_network(
    f"data/{city_name}/edges_{city_name}.csv",
    f"data/{city_name}/nodes_{city_name}.csv",
    real_network=True,
    keep_length=False
)

fig, ax = plt.subplots(1,2, figsize=(30,15))

plot_network(edge_df, node_df, node_id_col='id',base_width=1, node_label=True, title="Green overlap percentage", ax=ax[0], color_col_num="green_overlap_percentage", cmap="Greens")
plot_network(edge_df, node_df, node_id_col='id',base_width=1, node_label=True, title="Slope (%)", ax=ax[1], color_col_num="slope", cmap="bwr")
plt.tight_layout()
plt.show()

## gif creation
def extrait_numero(chemin_fichier):
    nom_fichier = os.path.basename(chemin_fichier)
    match = re.search(r"\d+", nom_fichier)
    return int(match.group()) if match else 0

fichier = sorted(glob.glob("output/optimization/test_parametres/2026-08-27_14-16-45/images/CAP_Sioux_Falls_test_-0.001_-2_bi_11/network/*.png"), key=extrait_numero)
images = [Image.open(f) for f in fichier]

images[0].save("output/optimization/test_parametres/2026-08-27_14-16-45/images/CAP_Sioux_Falls_test_-0.001_-2_bi_11/gif_network.gif",
               save_all=True, append_images=images[1:],duration=200, loop=0)
