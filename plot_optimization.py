import pandas as pd
import matplotlib.pyplot as plt
from utils_plotting import *
from utils_network_processing import *

edge_df, node_df = import_network("data/edges_small_grid_2.csv", "data/nodes_small_grid_2.csv")

# list_test_name = ["CAP_3_corner_4000_bi2"]
# for test_name in list_test_name:
#     plot_optimization_results(test_name, edge_df, node_df, save = True)
# plt.close('all')

# list_test_name = ['homog_500','homog_1000','random_500','random_1000','random_2000', 'random_1_2000','random_2_2000','random_3_2000','random_4_2000','random_5_2000', 'random_1_2000_bi2','random_2_2000_bi2','random_3_2000_bi2','random_4_2000_bi2','random_5_2000_bi2']
# fig,ax = plt.subplots(figsize=(10,10))
# for test_name in list_test_name:
#     results_df_opt = pd.read_csv(f"output/optimization/rgo_results_df_opt_{test_name}.csv")
#     results_df_opt.plot(kind='line', x="iteration", y="flow_of_removed_edge", ylabel="Bike flow of removed edge", grid=True, label=test_name,ax=ax)
# plt.show()
#
# list_budget=[10,25,35]
# plot_optimization_different_budgets(list_test_name, list_budget, save = True)

fig, ax = plt.subplots()
for test_name in ["CAP_2_corner_4000_bi2","CAP_3_corner_4000_bi2","corner_4000_bi2"]:
    results_df_opt = pd.read_csv(f"output/optimization/rgo_results_df_opt_{test_name}.csv")
    results_df_opt.plot(kind='line', x="iteration", y="modal_share_bike", ylabel="modal share bike", grid=True, label=test_name,ax=ax)
plt.show()