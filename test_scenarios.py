from network_processing import *
from plotting import *
import matplotlib.pyplot as plt

CURRENT_DIR = ""

edge_df, node_df = import_network(CURRENT_DIR + "data/edges_small_grid_2.csv", CURRENT_DIR + "data/nodes_small_grid_2.csv")
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(24, 16))

axes_flat = axes.flatten()

for i, scenario in enumerate([0, 1, 2, 3, 4, 5]):
    edge_df = apply_bike_infra_scenario(edge_df, scenario)
    plot_network(edge_df, node_df, ax=axes_flat[i],
                node_id_col='node',
                node_label=True,
                color_col_str='type_bike',
                base_width=1,
                legend=True,
                title=f"Scenario: {scenario}",
                figsize=(8, 8)),
plt.tight_layout()
plt.show()