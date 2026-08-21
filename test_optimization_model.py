import warnings
import logging
import random
import os

from utils_traffic import *
from utils_network_processing import *
from utils_plotting import *
from utils_od_matrix_generator import generate_od_df
from config import parameter
from utils_traffic import *
from utils_plotting import *
from utils_optimization import *
from datetime import datetime

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

list_ASC_bike = [-2]
list_beta_time = [-0.000075,-0.00008, -0.000085, -0.00009, -0.000095, -0.0001]
horodatage = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
city_name = "Sioux_Falls"
os.makedirs(f"output/optimization/test_parametres/{horodatage}")
edge_df, node_df = import_network(f"data/{city_name}/edges_{city_name}.csv", f"data/{city_name}/nodes_{city_name}.csv", real_network=True, keep_length=False)
od_df = pd.read_csv(f"data/{city_name}/od_{city_name}.csv")
od_df = convert_from_aequilibrae_od_matrix(od_df)

for ASC_bike in list_ASC_bike:
    for beta_time in list_beta_time:
        name_test = f"CAP_{city_name}_test_{beta_time}_{ASC_bike}"
        edge_df, node_df = import_network(f"data/{city_name}/edges_{city_name}.csv",
                                          f"data/{city_name}/nodes_{city_name}.csv", real_network=True,
                                          keep_length=False)
        dict_parameter = parameter("all")
        dict_parameter["ASC_bike"] = ASC_bike
        dict_parameter["beta_time"] = beta_time
        edge_df_results, results_df_opt = reverse_growth_optimization(edge_df, node_df, od_df, limit=100, CAP=True,
                                                                      from_scratch=True, custom_parameter_dict=dict_parameter)
        edge_df_results.to_csv(f"output/optimization/test_parametres/{horodatage}/rgo_edge_df_results_{name_test}.csv")
        results_df_opt.to_csv(f"output/optimization/test_parametres/{horodatage}/rgo_results_df_opt_{name_test}.csv")

# horodatage = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# beta_time = parameter("beta_time")
# ASC_bike = parameter('ASC_bike')
# city_name = "Sioux_Falls"
# name_test = f"{horodatage}_CAP_{city_name}_test_{beta_time}_{ASC_bike}"
# edge_df, node_df = import_network(f"data/{city_name}/edges_{city_name}.csv", f"data/{city_name}/nodes_{city_name}.csv", real_network=True, keep_length=False)
# od_df = pd.read_csv(f"data/{city_name}/od_{city_name}.csv")
# od_df = convert_from_aequilibrae_od_matrix(od_df)
# plot = True
# edge_df_results, results_df_opt = reverse_growth_optimization(edge_df, node_df, od_df, limit=2000, CAP=True, from_scratch=True)
# edge_df_results.to_csv(f"output/optimization/test_parametres/rgo_edge_df_results_{name_test}.csv")
# results_df_opt.to_csv(f"output/optimization/test_parametres/rgo_results_df_opt_{name_test}.csv")
