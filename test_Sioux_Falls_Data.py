from utils_plotting import *
from utils_network_processing import *
import matplotlib.pyplot as plt

edge_df, node_df = import_network("data/Sioux_Falls/edges_Sioux_Falls.csv", "data/Sioux_Falls/nodes_Sioux_Falls.csv")
plot_network(edge_df, node_df, node_label=True, title="Sioux Falls Network")
plt.show()