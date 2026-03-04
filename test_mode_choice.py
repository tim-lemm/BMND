import warnings
import logging
from utils_traffic import *
from utils_network_processing import *
from utils_plotting import *
from utils_od_matrix_generator import generate_od_df
from config import parameter

#TODO: update readme

CURRENT_DIR = ""

warnings.filterwarnings('ignore')
logging.getLogger("aequilibrae").setLevel(logging.ERROR)

edge_df, node_df = import_network(CURRENT_DIR + "data/edges_small_grid_2.csv", CURRENT_DIR + "data/nodes_small_grid_2.csv")

# parameters for mode choice
parameter_dict = parameter()
beta_time = parameter_dict['beta_time']
ASC_car = parameter_dict['ASC_car']
ASC_bike = parameter_dict['ASC_bike']
mu_mode = parameter_dict['mu_mode']
max_iter_mode_choice = parameter_dict['max_iter_mode_choice']
plot = True

size_od = max(node_df['node']) + 1

od_df = generate_od_df(size_od, od_scenario="RANDOM_OD", max_demand=2000)
for scenario in [0,1,2,3,4,5]:
    edge_df = apply_bike_infra_scenario(edge_df, scenario)
    plot_network(edge_df, node_df,
                 node_id_col='node',
                 node_label=True,
                 color_col_str='type_bike',
                 base_width=1,
                 legend=True,
                 title=f"Network with type of bike infrastructure, scenario {scenario}",
                 figsize=(8, 8))
    result_df, _, _,_,_ = mode_choice(edge_df,
                                                         node_df,
                                                         od_df,
                                                         beta_time,
                                                         ASC_car,
                                                         ASC_bike,
                                                         mu_mode=mu_mode,
                                                         max_iter_mode_choice=max_iter_mode_choice,
                                                         plot=plot)

result_all_df = pd.DataFrame(columns = ['number_of_bike_path',
                        'modal_share_car',
                        'modal_share_bike'])
# nbr_bike_lane = 0
#
# result_df, updated_od_car, updated_od_bike = mode_choice(edge_df,
#                                                          node_df,
#                                                          od_df,
#                                                          beta_time,
#                                                          ASC_car,
#                                                          ASC_bike,
#                                                          mu_mode=mu_mode,
#                                                          max_iter_mode_choice=max_iter_mode_choice,
#                                                          plot=False)
#
#
# new_row = pd.DataFrame([{
#     "number_of_bike_path": nbr_bike_lane,
#     "modal_share_car": result_df["modal_share_car"].iloc[-1],
#     "modal_share_bike": result_df["modal_share_bike"].iloc[-1]
# }])
# result_all_df = pd.concat([result_all_df, new_row], ignore_index=True)
#
# for i, edge in edge_df.iterrows():
#
#     a_node = edge["a_node"]
#     b_node = edge["b_node"]
#     print(a_node, b_node)
#     edge_df = change_type_bike_infra(edge_df, "bike_path",a_node,b_node)
#     nbr_bike_lane += 1
#     result_df, updated_od_car, updated_od_bike = mode_choice(edge_df,
#                                                             node_df,
#                                                             od_df,
#                                                             beta_time,
#                                                             ASC_car,
#                                                             ASC_bike,
#                                                             mu_mode=mu_mode,
#                                                             max_iter_mode_choice=10,
#                                                             plot=False)
#
#     new_row = pd.DataFrame([{
#                 "number_of_bike_path": nbr_bike_lane,
#                 "modal_share_car": result_df["modal_share_car"].iloc[-1],
#                 "modal_share_bike": result_df["modal_share_bike"].iloc[-1]
#             }])
#     result_all_df = pd.concat([result_all_df, new_row], ignore_index=True)
#     edge_df = change_type_bike_infra(edge_df, "bike_path", b_node, a_node)
#     nbr_bike_lane += 1
#     result_df, updated_od_car, updated_od_bike = mode_choice(edge_df,
#                                                                  node_df,
#                                                                  od_df,
#                                                                  beta_time,
#                                                                  ASC_car,
#                                                                  ASC_bike,
#                                                                  mu_mode=mu_mode,
#                                                                  max_iter_mode_choice=10,
#                                                                  plot=False)
#
#     new_row = pd.DataFrame([{
#             "number_of_bike_path": nbr_bike_lane,
#             "modal_share_car": result_df["modal_share_car"].iloc[-1],
#             "modal_share_bike": result_df["modal_share_bike"].iloc[-1]
#         }])
#     result_all_df = pd.concat([result_all_df, new_row], ignore_index=True)
#
# result_all_df.plot(x="number_of_bike_path", y="modal_share_car", kind="line")
# result_all_df.to_csv("output/test_mc_df.csv")
# plt.show()