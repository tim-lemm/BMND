import warnings
import logging
import random

from utils_traffic import *
from utils_network_processing import *
from utils_plotting import *
from utils_od_matrix_generator import generate_od_df
from config import parameter
from utils_traffic import *
from utils_plotting import *
from utils_optimization import *

warnings.filterwarnings('ignore')
logging.getLogger("aequilibrae").setLevel(logging.ERROR)

# list_test_name = ["grid","H","tunnel","tunnel_ng"]
# list_KPI = ["modal_share_bike", "travel_time_bike", "travel_time_car"]
# list_CAP = [False,True]

# for CAP in list_CAP:
#     for test_name in list_test_name:
#         edge_df, node_df, od_df = load_test_scenario(test_name, "CORNER_2")
#         if CAP:
#             test_name = test_name + "_CAP"
#         edge_df_results, results_df_opt = reverse_growth_optimization(edge_df, node_df, od_df, limit=48, CAP=CAP)
#         edge_df_results.to_csv(f"output/_hEART_article/csv/optimization/{test_name}_rgo_edge_results.csv")
#         results_df_opt.to_csv(f"output/_hEART_article/csv/optimization/{test_name}_rgo_results_df_opt.csv")
#         edge_df_results = pd.read_csv(f"output/_hEART_article/csv/optimization/{test_name}_rgo_edge_results.csv")
#         results_df_opt = pd.read_csv(f"output/_hEART_article/csv/optimization/{test_name}_rgo_results_df_opt.csv")
#         plot_optimization_results(test_name, edge_df, node_df, save=True, file_path = "output/_hEART_article/figures/", edge_df_results = edge_df_results, results_df_opt = results_df_opt)
#         plt.close("all")
#         results_test_random_df = test_random(edge_df, node_df, od_df, CAP=CAP)
#         results_test_random_df.to_csv(f'output/_hEART_article/csv/random/{test_name}_results_test_random.csv')

# list_speed_bike = [5,10,15,20,25]
# list_ASC_bike = [0,-1,-2,-2.5,-3,-10]
# list_beta_time = [-0.0002,-0.00021,-0.00022,-0.00023,-0.000235,-0.00024]
#
# test_name = "grid"
# edge_df, node_df, od_df = load_test_scenario(test_name, "CORNER_2")
# parameter_dict = parameter()
# for speed_bike in list_speed_bike:
#     for ASC_bike in list_ASC_bike:
#         for beta_time in list_beta_time:
#             parameter_dict['speed_bike'] = speed_bike
#             parameter_dict['ASC_bike'] = ASC_bike
#             parameter_dict['beta_time'] = beta_time
#             edge_df_results, results_df_opt = reverse_growth_optimization(edge_df, node_df, od_df, limit=48, CAP=True, custom_parameter_dict=parameter_dict)
#             edge_df_results.to_csv(f"output/_hEART_article/csv/sensitivity_analysis/{speed_bike}_{ASC_bike}_{beta_time}_rgo_edge_results.csv")
#             results_df_opt.to_csv(f"output/_hEART_article/csv//sensitivity_analysis/{speed_bike}_{ASC_bike}_{beta_time}_rgo_results_df_opt.csv")

edge_df, node_df = import_network("data/Sioux_Falls/edges_Sioux_Falls.csv", "data/Sioux_Falls/nodes_Sioux_Falls.csv", real_network=True)
od_df = pd.read_csv("data/Sioux_Falls/SiouxFalls_od.csv")
od_df = convert_from_aequilibrae_od_matrix(od_df)
plot = False

edge_df_results, results_df_opt = reverse_growth_optimization(edge_df, node_df, od_df, limit=80, CAP=False)
edge_df_results.to_csv(f"output/optimization/rgo_edge_df_results_SF.csv")
results_df_opt.to_csv(f"output/optimization/rgo_results_df_opt_SF.csv")
