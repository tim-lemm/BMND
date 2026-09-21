import warnings
import logging
import random
import os
import pandas as pd
from utils_traffic import *
from utils_network_processing import *
from utils_plotting import *
from utils_od_matrix_generator import generate_od_df
from config import parameter
from utils_traffic import *
from utils_plotting import *
from utils_optimization import *
from datetime import datetime
import itertools
from tqdm import tqdm
import csv

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

# list_ASC_bike = [-2]
# # list_beta_time = [-0.005,-0.0001,-0.0005,-0.00001]
# list_beta_time = [-0.001]
# list_coef_map_num = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
# horodatage = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# city_name = "Sioux_Falls"
# os.makedirs(f"output/optimization/test_parametres/{horodatage}")
# edge_df, node_df = import_network(f"data/{city_name}/edges_{city_name}.csv", f"data/{city_name}/nodes_{city_name}.csv", real_network=True, keep_length=False)
# od_df = pd.read_csv(f"data/{city_name}/od_{city_name}.csv")
# od_df = convert_from_aequilibrae_od_matrix(od_df)
# for coef_map_num in list_coef_map_num:
#     for ASC_bike in list_ASC_bike:
#         for beta_time in list_beta_time:
#             name_test = f"CAP_{city_name}_test_{beta_time}_{ASC_bike}_bi_{coef_map_num}"
#             print(f"Testing {beta_time} - {ASC_bike} - {coef_map_num}")
#             edge_df, node_df = import_network(f"data/{city_name}/edges_{city_name}.csv",
#                                               f"data/{city_name}/nodes_{city_name}.csv", real_network=True,
#                                               keep_length=False)
#             dict_parameter = parameter("all")
#             dict_parameter["ASC_bike"] = ASC_bike
#             dict_parameter["beta_time"] = beta_time
#             edge_df_results, results_df_opt = reverse_growth_optimization(edge_df, node_df, od_df, limit=100, CAP=True,
#                                                                           from_scratch=True, custom_parameter_dict=dict_parameter, coef_map_num=coef_map_num)
#             edge_df_results.to_csv(f"output/optimization/test_parametres/{horodatage}/rgo_edge_df_results_{name_test}.csv")
#             results_df_opt.to_csv(f"output/optimization/test_parametres/{horodatage}/rgo_results_df_opt_{name_test}.csv")

horodatage = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
os.makedirs(f"output/optimization/test_parametres/{horodatage}", exist_ok=True)
beta_time = -0.001
# list_beta_time = [-0.0009,-0.001,-0.0011]
# ASC_bike = -2
list_ASC_bike = [-1.98, -1.99, -2, -2.01, -2.02]
dict_parameter = parameter("all")
list_coef_map_num = [20,31,25]
for coef_map_num in list_coef_map_num:
    for ASC_bike in list_ASC_bike :
        dict_parameter["beta_time"] = beta_time
        dict_parameter["ASC_bike"] = ASC_bike
        city_name = "Sioux_Falls"
        name_test = f"CAP_{city_name}_test_{beta_time}_{ASC_bike}_bi_{coef_map_num}"
        edge_df, node_df = import_network(f"data/{city_name}/edges_{city_name}.csv", f"data/{city_name}/nodes_{city_name}.csv", real_network=True, keep_length=False)
        od_df = pd.read_csv(f"data/{city_name}/od_{city_name}.csv")
        od_df = convert_from_aequilibrae_od_matrix(od_df)
        plot = False
        edge_df_results, results_df_opt = reverse_growth_optimization(edge_df, node_df, od_df, limit=100, CAP=True,
                                                                                   from_scratch=True, custom_parameter_dict=dict_parameter, coef_map_num=coef_map_num)
        edge_df_results.to_csv(f"output/optimization/test_parametres/{horodatage}/rgo_edge_df_results_{name_test}.csv")
        results_df_opt.to_csv(f"output/optimization/test_parametres/{horodatage}/rgo_results_df_opt_{name_test}.csv")

# list_ASC_bike = [-2]
# list_beta_time = [-0.001]
# list_coef_map_num = [11,16,9]
# list_i = range(1,10)
# data = []
#
# horodatage = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# city_name = "Sioux_Falls"
# os.makedirs(f"output/optimization/test_parametres/{horodatage}")
#
# edge_df, node_df = import_network(
#     f"data/{city_name}/edges_{city_name}.csv",
#     f"data/{city_name}/nodes_{city_name}.csv",
#     real_network=True,
#     keep_length=False
# )
# od_df = pd.read_csv(f"data/{city_name}/od_{city_name}.csv")
# od_df = convert_from_aequilibrae_od_matrix(od_df)
#
# # Regroupement des paramètres en une liste unique de combinaisons
# combinations = list(itertools.product(list_coef_map_num, list_ASC_bike, list_beta_time, list_i))
#
# # Boucle avec barre de progression et estimation dynamique du temps restant
# for coef_map_num, ASC_bike, beta_time, i in tqdm(combinations, desc="Optimisation"):
#     print("\n")
#     name_test = f"CAP_{city_name}_bi_{coef_map_num}_test_{i}"
#
#     # tqdm.write évite de casser la barre de progression dans la console
#     print(f"\n--- Testing {beta_time} - {ASC_bike} - {coef_map_num} ---\n")
#
#     edge_df, node_df = import_network(
#         f"data/{city_name}/edges_{city_name}.csv",
#         f"data/{city_name}/nodes_{city_name}.csv",
#         real_network=True,
#         keep_length=False
#     )
#     edge_df["type_bike"] = None
#     edge_df["existing_bike_infra"] = False
#     liste_index = random.sample(range(1,77),10)
#     data.append([i] + liste_index)
#     change_type_bike_infra_with_index(edge_df, "bike_path", liste_index)
#     edge_df['existing_bike_infra'] = edge_df['type_bike']=="bike_path"
#
#     dict_parameter = parameter("all")
#     dict_parameter["ASC_bike"] = ASC_bike
#     dict_parameter["beta_time"] = beta_time
#
#     edge_df_results, results_df_opt = reverse_growth_optimization(
#         edge_df, node_df, od_df, limit=100, CAP=True,
#         from_scratch=False, custom_parameter_dict=dict_parameter, coef_map_num=coef_map_num
#     )
#
#     edge_df_results.to_csv(f"output/optimization/test_parametres/{horodatage}/rgo_edge_df_results_{name_test}.csv")
#     results_df_opt.to_csv(f"output/optimization/test_parametres/{horodatage}/rgo_results_df_opt_{name_test}.csv")
#
# with open(f"output/optimization/test_parametres/{horodatage}/tirage.csv", mode='w', newline='', encoding="utf-8") as f:
#     writer = csv.writer(f)
#     writer.writerow(["i", "N1", "N2", "N3", "N4", "N5"])
#     writer.writerows(data)