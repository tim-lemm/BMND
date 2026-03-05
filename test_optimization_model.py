import warnings
import logging

from IPython.core.display_functions import display

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
size_od = max(node_df['node']) + 1
list_i = [2,3,4,5]
for i in list_i:
    od_df = generate_od_df(size_od, od_scenario="RANDOM_OD", max_demand=2000,seed=i)
    test_name = f"random_{i}_2000"

    edge_df_results, results_df_opt = reverse_growth_optimization(edge_df, node_df, od_df)

    edge_df_results.to_csv(f"output/optimization/rgo_edge_df_results_{test_name}.csv")
    results_df_opt.to_csv(f"output/optimization/rgo_results_df_opt_{test_name}.csv")