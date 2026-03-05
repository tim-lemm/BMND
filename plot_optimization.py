import pandas as pd
import matplotlib.pyplot as plt
from utils_plotting import *
from utils_network_processing import *

edge_df, node_df = import_network("data/edges_small_grid_2.csv", "data/nodes_small_grid_2.csv")

list_test_name = ['random_1_2000','random_2_2000','random_3_2000','random_4_2000','random_5_2000']
for test_name in list_test_name:
    plot_optimization_results(test_name, edge_df, node_df, save = True)
plt.close('all')

list_test_name = ['homog_1000','random_2000', 'random_1_2000','random_2_2000','random_3_2000','random_4_2000','random_5_2000']
fig,ax = plt.subplots(figsize=(10,10))
for test_name in list_test_name:
    results_df_opt = pd.read_csv(f"output/optimization/rgo_results_df_opt_{test_name}.csv")
    results_df_opt.plot(kind='line', x="iteration", y="flow_of_removed_edge", ylabel="Bike flow", grid=True, label=f"Results for {test_name}",ax=ax)
plt.show()
