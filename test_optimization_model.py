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

list_test_name = ["grid","H","tunnel","tunnel_ng"]
list_KPI = ["modal_share_bike", "travel_time_bike", "travel_time_car"]
list_CAP = [False,True]

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

