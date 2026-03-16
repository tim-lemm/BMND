import warnings
import logging

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

#import network
edge_df, node_df = import_network("data/edges_small_grid_2.csv", "data/nodes_small_grid_2.csv")

#od matrix creation
size_od = max(node_df['id']) + 1
list_demand = [4000]
for demand in list_demand:
    od_df = generate_od_df(size_od, od_scenario="CORNER_2", max_demand=demand)
    test_name = f"CAP_1_corner_{demand}_bi2"

    edge_df_results, results_df_opt = reverse_growth_optimization(edge_df, node_df, od_df, limit=48)

    edge_df_results.to_csv(f"output/optimization/rgo_edge_df_results_{test_name}.csv")
    results_df_opt.to_csv(f"output/optimization/rgo_results_df_opt_{test_name}.csv")