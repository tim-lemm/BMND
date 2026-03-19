import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import legend

from utils_plotting import *
from utils_network_processing import *

# edge_df, node_df = import_network("data/_old/edges_small_grid_3.csv", "data/_old/nodes_small_grid_3.csv")
#
# list_test_name = ["grid","H","tunnel","tunnel_ng"]
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

# fig, ax = plt.subplots()
# for test_name in ["CAP_2_tunnel_corner_2_4000_bi2","tunnel_corner_2_4000_bi2"]:
#     results_df_opt = pd.read_csv(f"output/optimization/rgo_results_df_opt_{test_name}.csv")
#     results_df_opt.plot(kind='line', x="iteration", y="modal_share_bike", ylabel="modal share bike", grid=True, label=test_name,ax=ax)
# plt.show()


# list_test_name = ["grid_CAP", "H_CAP", "tunnel_CAP", "tunnel_ng_CAP"]
# list_color = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']
#
# fig, ax1 = plt.subplots(figsize=(10, 6))
# # Create the second axes that shares the same x-axis
# ax2 = ax1.twinx()
#
# for test_name, color in zip(list_test_name, list_color):
#      # Load data
#      fp = f"output/_hEART_article/csv/optimization/{test_name}_rgo_results_df_opt.csv"
#      df = pd.read_csv(fp)
#
#      # Plot primary Y (Solid line)
#      df.plot(kind='line', x="nbr_bike_lanes", y="modal_share_bike",
#              ax=ax1, color=color, label=test_name, linewidth=0.8)
#
#      # Plot secondary Y (Dashed line)
#      df.plot(kind='line', x="nbr_bike_lanes", y="flow_of_removed_edge",
#              ax=ax2, color=color, linestyle='--', legend=False, linewidth=0.8)
#
#
# # Formatting
# ax1.set_xlabel("Number of dedicated bike lanes")
# ax1.set_ylabel("Bicycle modal share (%)", color='black')
# ax2.set_ylabel("Flow of removed edge", color='black')
# ax1.grid(True, alpha=0.3)
#
# # Handle combined legend if necessary (ax1 will only show solid lines)
# ax1.legend(title="Test Scenario", bbox_to_anchor=(1, 0.7))
#
#
# plt.tight_layout()
# # plt.show()
#
# plt.savefig("output/_hEART_article/figures/_results/CAP_mode_share_nbr_bike_lane.png")




# list_test_name = ["grid", "H", "tunnel", "tunnel_ng"]
# list_color = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']
#
# fig, ax1 = plt.subplots(figsize=(10, 6))
#
# for test_name, color in zip(list_test_name, list_color):
#     # Chargement des données
#     df = pd.read_csv(f"output/_hEART_article/csv/optimization/{test_name}_rgo_results_df_opt.csv")
#     df_CAP = pd.read_csv(f"output/_hEART_article/csv/optimization/{test_name}_CAP_rgo_results_df_opt.csv")
#
#     # Scénario Standard (Plein)
#     df.plot(kind='line', x="nbr_bike_lanes", y="modal_share_bike",
#              ax=ax1, color=color, linestyle='--', label=test_name, linewidth=0.8)
#
#     # Scénario CAP (Pointillé)
#     df_CAP.plot(kind='line', x="nbr_bike_lanes", y="modal_share_bike",
#              ax=ax1, color=color, label=test_name+" with capacity", linewidth=0.8)
#
#
# ax1.legend(bbox_to_anchor=(1, 0.8), title="Test Scenario",labelspacing=0.3, fontsize='small')
#
# # Mise en forme finale
# ax1.set_xlabel("Number of dedicated bike lanes")
# ax1.set_ylabel("Bicycle modal share (%)")
# ax1.grid(True, alpha=0.3)
#
# plt.tight_layout()
# # plt.show()
#
# plt.savefig("output/_hEART_article/figures/_results/comparison_CAP_mode_share_nbr_bike_lane.png")

fig, ax = plt.subplots(2,2, figsize=(20,20))

edge_df = pd.read_csv("data/edges_tunnel.csv")
edge_df_results_tunnel = pd.read_csv("output/_hEART_article/csv/optimization/tunnel_CAP_rgo_edge_results.csv")
results_df_tunnel = pd.read_csv("output/_hEART_article/csv/optimization/tunnel_CAP_rgo_results_df_opt.csv")
results_df_tunnel.drop("Unnamed: 0", axis=1, inplace=True)
results_df_tunnel = results_df_tunnel.iloc[1:].reset_index(drop=True)
results_df_tunnel["index_removed"] = results_df_tunnel["index_removed"].apply(ast.literal_eval)
results_df_tunnel = results_df_tunnel.explode('index_removed')
edge_df_results_tunnel = edge_df_results_tunnel.merge(results_df_tunnel, how="inner", left_on="id", right_on="index_removed")
edge_df_results_tunnel.index = edge_df["id"]
edge_df_results_tunnel.drop(
        ["nbr_bike_lanes", "nbr_none_bike_lanes", "modal_share_car", "modal_share_bike",
         "index_removed",
         "flow_of_removed_edge"], axis=1, inplace=True)
edge_df_results_tunnel.rename(columns={'iteration': 'iteration_of_removal'}, inplace=True)

edge_df_results_tunnel_ng = pd.read_csv("output/_hEART_article/csv/optimization/tunnel_ng_CAP_rgo_edge_results.csv")
results_df_tunnel_ng = pd.read_csv("output/_hEART_article/csv/optimization/tunnel_ng_CAP_rgo_results_df_opt.csv")
results_df_tunnel_ng.drop("Unnamed: 0", axis=1, inplace=True)
results_df_tunnel_ng = results_df_tunnel_ng.iloc[1:].reset_index(drop=True)
results_df_tunnel_ng["index_removed"] = results_df_tunnel_ng["index_removed"].apply(ast.literal_eval)
results_df_tunnel_ng = results_df_tunnel_ng.explode('index_removed')
edge_df_results_tunnel_ng = edge_df_results_tunnel_ng.merge(results_df_tunnel_ng, how="inner", left_on="id", right_on="index_removed")
edge_df_results_tunnel_ng.index = edge_df["id"]
edge_df_results_tunnel_ng.drop(
        ["nbr_bike_lanes", "nbr_none_bike_lanes", "modal_share_car", "modal_share_bike",
         "index_removed",
         "flow_of_removed_edge"], axis=1, inplace=True)
edge_df_results_tunnel_ng.rename(columns={'iteration': 'iteration_of_removal'}, inplace=True)

node_df = pd.read_csv("data/nodes_tunnel.csv")
plot_network(edge_df_results_tunnel, node_df, node_id_col='id',
                     node_label=True,
                     color_col_num='iteration_of_removal',
                     base_width=1,
                     legend=True,
                     title=f"With a park (tunnel)", ax=ax[0,0])
plot_network(edge_df_results_tunnel_ng, node_df, node_id_col='id',
                     node_label=True,
                     color_col_num='iteration_of_removal',
                     base_width=1,
                     legend=True,
                     title=f"Without a park (tunnel_ng)", ax=ax[0,1])
plot_network(edge_df_results_tunnel, node_df, node_id_col='id',
             node_label=True,
                 color_col_num='coef_bi_0',base_width=1,cmap="hot_r",ax=ax[1,0], title=f"Bikeability coefficient \n (tunnel, bicycle lanes on all edges)")
plot_network(edge_df_results_tunnel_ng, node_df, node_id_col='id',
             node_label=True,
                 color_col_num='coef_bi_0',base_width=1,cmap="hot_r",ax=ax[1,1],title=f"Bikeability coefficient \n (tunnel_ng, bicycle lanes on all edges)", vmin= 0.2)
plt.savefig("output/_hEART_article/figures/_results/CAP_comparaison_tunnels.png")
# plt.show()
# KPI = "modal_share_bike"
# CAP = False
#
# for test_name, color in zip(list_test_name, list_color):
#     if CAP:
#         test_name = test_name + "_CAP"
#     results_test_random_df = pd.read_csv(f'output/_hEART_article/csv/random/{test_name}_results_test_random.csv')
#     results_df_opt = pd.read_csv(f"output/_hEART_article/csv/optimization/{test_name}_rgo_results_df_opt.csv")
#     KPI_budget_10 = results_df_opt[results_df_opt["nbr_bike_lanes"] == 10][KPI].iloc[0]
#     results_test_random_df[KPI].plot.kde(label=test_name, figsize = (15,10))
#     plt.axvline(x=KPI_budget_10, linestyle='--', linewidth=2, color=color)
# plt.grid()
# plt.xlabel("Bike Modal Share")
# plt.title(f"Bike Modal Share for different network.")
# plt.legend()
# plt.savefig(f"output/_hEART_article/figures/_random/{KPI}{"_CAP" if CAP else ""}.png")
#
# CAP = True
#
# for test_name, color in zip(list_test_name, list_color):
#     if CAP:
#         test_name = test_name + "_CAP"
#     results_test_random_df = pd.read_csv(f'output/_hEART_article/csv/random/{test_name}_results_test_random.csv')
#     results_df_opt = pd.read_csv(f"output/_hEART_article/csv/optimization/{test_name}_rgo_results_df_opt.csv")
#     KPI_budget_10 = results_df_opt[results_df_opt["nbr_bike_lanes"] == 10][KPI].iloc[0]
#     results_test_random_df[KPI].plot.kde(label=test_name, figsize = (15,10))
#     plt.axvline(x=KPI_budget_10, linestyle='--', linewidth=2, color=color)
# plt.grid()
# plt.xlabel(KPI)
# plt.title(f"{KPI.strip("_")} for different network.")
# plt.legend()
# plt.savefig(f"output/_hEART_article/figures/_random/{KPI}{"_CAP" if CAP else ""}.png")
#
# KPI = "travel_time_bike"
# CAP = True
#
# for test_name, color in zip(list_test_name, list_color):
#     if CAP:
#         test_name = test_name + "_CAP"
#     results_test_random_df = pd.read_csv(f'output/_hEART_article/csv/random/{test_name}_results_test_random.csv')
#     results_df_opt = pd.read_csv(f"output/_hEART_article/csv/optimization/{test_name}_rgo_results_df_opt.csv")
#     edge_result_df = pd.read_csv(f"output/_hEART_article/csv/optimization/{test_name}_rgo_edge_results.csv")
#     iteration = max(results_df_opt["iteration"])-10
#     KPI_budget_10 = (
#             edge_result_df[f"travel_time_bike_{iteration}"] * edge_result_df[f"flow_bike_iteration_{iteration}"]
#     ).sum()
#     results_test_random_df[KPI].plot.kde(label=test_name, figsize = (15,10))
#     plt.axvline(x=KPI_budget_10, linestyle='--', linewidth=2, color=color)
# plt.grid()
# plt.xlabel(KPI)
# plt.title(f"{KPI.strip("_")} for different network.")
# plt.legend()
# plt.savefig(f"output/_hEART_article/figures/_random/{KPI}{"_CAP" if CAP else ""}.png")
#
# CAP = False
#
# for test_name, color in zip(list_test_name, list_color):
#     if CAP:
#         test_name = test_name + "_CAP"
#     results_test_random_df = pd.read_csv(f'output/_hEART_article/csv/random/{test_name}_results_test_random.csv')
#     results_df_opt = pd.read_csv(f"output/_hEART_article/csv/optimization/{test_name}_rgo_results_df_opt.csv")
#     edge_result_df = pd.read_csv(f"output/_hEART_article/csv/optimization/{test_name}_rgo_edge_results.csv")
#     iteration = max(results_df_opt["iteration"])-10
#     KPI_budget_10 = (
#             edge_result_df[f"travel_time_bike_{iteration}"] * edge_result_df[f"flow_bike_iteration_{iteration}"]
#     ).sum()
#     results_test_random_df[KPI].plot.kde(label=test_name, figsize = (15,10))
#     plt.axvline(x=KPI_budget_10, linestyle='--', linewidth=2, color=color)
# plt.grid()
# plt.xlabel(KPI)
# plt.title(f"{KPI.strip("_")} for different network.")
# plt.legend()
# plt.savefig(f"output/_hEART_article/figures/_random/{KPI}{"_CAP" if CAP else ""}.png")
#
# KPI = "travel_time_car"
# CAP = True
#
# for test_name, color in zip(list_test_name, list_color):
#     if CAP:
#         test_name = test_name + "_CAP"
#     results_test_random_df = pd.read_csv(f'output/_hEART_article/csv/random/{test_name}_results_test_random.csv')
#     results_df_opt = pd.read_csv(f"output/_hEART_article/csv/optimization/{test_name}_rgo_results_df_opt.csv")
#     edge_result_df = pd.read_csv(f"output/_hEART_article/csv/optimization/{test_name}_rgo_edge_results.csv")
#     iteration = max(results_df_opt["iteration"])-10
#     KPI_budget_10 = (
#             edge_result_df[f"travel_time_car_{iteration}"] * edge_result_df[f"flow_car_iteration_{iteration}"]
#     ).sum()
#     results_test_random_df[KPI].plot.kde(label=test_name, figsize = (15,10))
#     plt.axvline(x=KPI_budget_10, linestyle='--', linewidth=2, color=color)
# plt.grid()
# plt.xlabel(KPI)
# plt.title(f"{KPI.strip("_")} for different network.")
# plt.legend()
# plt.savefig(f"output/_hEART_article/figures/_random/{KPI}{"_CAP" if CAP else ""}.png")
#
# CAP = False
#
# for test_name, color in zip(list_test_name, list_color):
#     if CAP:
#         test_name = test_name + "_CAP"
#     results_test_random_df = pd.read_csv(f'output/_hEART_article/csv/random/{test_name}_results_test_random.csv')
#     results_df_opt = pd.read_csv(f"output/_hEART_article/csv/optimization/{test_name}_rgo_results_df_opt.csv")
#     edge_result_df = pd.read_csv(f"output/_hEART_article/csv/optimization/{test_name}_rgo_edge_results.csv")
#     iteration = max(results_df_opt["iteration"])-10
#     KPI_budget_10 = (
#             edge_result_df[f"travel_time_car_{iteration}"] * edge_result_df[f"flow_car_iteration_{iteration}"]
#     ).sum()
#     results_test_random_df[KPI].plot.kde(label=test_name, figsize = (15,10))
#     plt.axvline(x=KPI_budget_10, linestyle='--', linewidth=2, color=color)
# plt.grid()
# plt.xlabel(KPI)
# plt.title(f"{KPI.strip("_")} for different network.")
# plt.legend()
# plt.savefig(f"output/_hEART_article/figures/_random/{KPI}{"_CAP" if CAP else ""}.png")