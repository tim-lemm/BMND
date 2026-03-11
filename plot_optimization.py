import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from utils_plotting import *
from utils_network_processing import *
import ast

edge_df, node_df = import_network("data/edges_small_grid_2.csv", "data/nodes_small_grid_2.csv")

# list_test_name = ['random_1_2000_bi2','random_2_2000_bi2','random_3_2000_bi2','random_4_2000_bi2','random_5_2000_bi2']
# for test_name in list_test_name:
#     plot_optimization_results(test_name, edge_df, node_df, save = True)
# plt.close('all')
#
# list_test_name = ['homog_500','homog_1000','random_500','random_1000','random_2000', 'random_1_2000','random_2_2000','random_3_2000','random_4_2000','random_5_2000', 'random_1_2000_bi2','random_2_2000_bi2','random_3_2000_bi2','random_4_2000_bi2','random_5_2000_bi2']
# fig,ax = plt.subplots(figsize=(10,10))
# for test_name in list_test_name:
#     results_df_opt = pd.read_csv(f"output/optimization/rgo_results_df_opt_{test_name}.csv")
#     results_df_opt.plot(kind='line', x="iteration", y="flow_of_removed_edge", ylabel="Bike flow of removed edge", grid=True, label=test_name,ax=ax)
# plt.show()

list_budget=[1,10,20]
# plot_optimization_different_budgets(list_test_name, list_budget, save = False)

edge_df = pd.read_csv("data/Delft/edges.csv")
edge_df = initialization_delft(edge_df)
node_df = pd.read_csv("data/Delft/nodes.csv")
od_df = pd.read_csv("data/Delft/od.csv")
results_df_opt = pd.read_csv(f"output/optimization/DELFT/rgo_results_df_opt.csv")
edge_df_results = pd.read_csv(f"output/optimization/DELFT/rgo_edge_df_results.csv")


results_df_opt.drop("Unnamed: 0", axis=1, inplace=True)
results_df_opt = results_df_opt.iloc[1:].reset_index(drop=True)
results_df_opt["index_removed"] = results_df_opt["index_removed"].apply(ast.literal_eval)
results_df_opt = results_df_opt.explode('index_removed')
edge_df = edge_df.merge(results_df_opt, how="inner", left_on="id", right_on="index_removed")
edge_df.index = edge_df["Unnamed: 0"]
edge_df.drop(
            ["Unnamed: 0", "nbr_bike_lanes", "nbr_none_bike_lanes", "modal_share_car", "modal_share_bike",
             "index_removed",
             "flow_of_removed_edge"], axis=1, inplace=True)
edge_df.rename(columns={'iteration': 'iteration_of_removal'}, inplace=True)
fig, ax = plt.subplots(3, len(list_budget), figsize=(4*len(list_budget), 10))
i = 0
for budget in list_budget:
    max_budget = max(edge_df["iteration_of_removal"])
    iteration_corresponding_to_budget = max_budget - budget

    mask = edge_df["iteration_of_removal"] >= iteration_corresponding_to_budget
    list_index_of_bike_infra = edge_df.index[mask].tolist()

    mappable = cm.ScalarMappable(cmap='Greens')
    mappable.set_array([])
    cb = plt.colorbar(mappable, ax=ax[0,i])
    cb.ax.set_visible(False)
    edge_df = change_type_bike_infra_with_index(edge_df, "bike_path", list_index_of_bike_infra)
    plot_network(edge_df, node_df, node_id_col='id',
                         node_label=False,
                         color_col_str='type_bike',
                         base_width=1,
                         legend=True,
                 node_size=0,
                         title=f"Network for a budget of {budget*25}", ax=ax[0,i])
    plot_network(edge_df_results, node_df, width_col=f'flow_bike_iteration_{iteration_corresponding_to_budget}',
                  color_col_num=f'flow_bike_iteration_{iteration_corresponding_to_budget}', cmap='Greens',
                  title=f'Bike flows - budget: {budget*25}', node_size=0, colorbar_label='Flow (bikes)',
                  base_width=0.1, width_scale=10, ax=ax[1, i])
    plot_network(edge_df_results, node_df, width_col=f'flow_car_iteration_{iteration_corresponding_to_budget}',
                  color_col_num=f'flow_car_iteration_{iteration_corresponding_to_budget}', cmap='Reds',
                  title=f'Car flows - budget: {budget*25}', node_size=0, colorbar_label='Flow (car)',
                  base_width=0.1, width_scale=10, ax=ax[2, i])
    i += 1
plt.tight_layout(rect=[0.02, 0.03, 0.98, 0.95])
plt.suptitle(f'Networks for Delft', fontsize=20, fontweight='bold')
plt.show()

plot_network(edge_df, node_df, node_id_col='id',
                     node_label=True,
                     color_col_num='iteration_of_removal',
                     base_width=1,
                     legend=True,
                     title=f"Network with iteration of removal")
plt.show()
ax = results_df_opt.plot(kind='line', x="iteration", y="flow_of_removed_edge",
                             color='blue', label="Bike flow", grid=True, title=f"Results")

results_df_opt.plot(kind='line', x="iteration", y="modal_share_bike",
                        color='red', label="Modal share bike", secondary_y=True, ax=ax)

plt.show()
results_df_opt.plot(x='iteration', y='average_bi_coef', grid=True, title=f"Average bike coefficient for each iteration")
plt.show()