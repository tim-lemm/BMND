import warnings
import logging
from utils_traffic import *
from utils_network_processing import *
from utils_plotting import *
from utils_od_matrix_generator import generate_od_df
from config import parameter
import random
import pandas as pd

#TODO: update readme


warnings.filterwarnings('ignore')
logging.getLogger("aequilibrae").setLevel(logging.ERROR)

edge_df, node_df = import_network("data/Sioux_Falls/edges_Sioux_Falls.csv", "data/Sioux_Falls/nodes_Sioux_Falls.csv")
od_df = pd.read_csv("data/Sioux_Falls/SiouxFalls_od.csv")
od_df = convert_from_aequilibrae_od_matrix(od_df)
# parameters for mode choice
parameter_dict = parameter()
beta_time = parameter_dict['beta_time']
ASC_car = parameter_dict['ASC_car']
ASC_bike = parameter_dict['ASC_bike']-1
mu_mode = parameter_dict['mu_mode']
max_iter_mode_choice = parameter_dict['max_iter_mode_choice']
plot = False

size_od = max(node_df['id']) + 1

# od_df = generate_od_df(size_od, od_scenario="CORNER_2", max_demand=4000)

plot_od_matrix(convert_to_eaquilibrae_od_matrix(od_df),edge_df,node_df)
# plot_od_matrix(od_df,edge_df,node_df)
plt.show()

results_df, updated_od_car, updated_od_bike, prob_matrice_car, prob_matrice_bike, edge_df = mode_choice(edge_df,
                node_df,
                od_df,
                beta_time=beta_time,
                ASC_car=ASC_car,
                ASC_bike=ASC_bike,
                mu_mode=mu_mode,
                max_iter_mode_choice=max_iter_mode_choice,
                plot=True,
                return_network=True,
                CAP = True)