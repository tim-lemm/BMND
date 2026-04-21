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

edge_df, node_df = import_network("data/Sioux_Falls/edges_Sioux_Falls.csv", "data/Sioux_Falls/nodes_Sioux_Falls.csv", real_network=True)
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

# def bi_coef(traffic, weight=1, bias=0):
#     if traffic < weight * (6000 + bias):
#         return 0.8
#     elif traffic >= weight * (8000 + bias):
#         return 1.4
#     elif weight * (6000 + bias) <= traffic < weight * (7500 + bias):
#         return 1
#     elif weight * (7500 + bias) <= traffic < weight * (8000 + bias):
#         return 1.2
#     else:
#         return 0
#
# traffics = list(range(1,50000))
#
# list_bias = [0,5000]
# list_weight = [1,1.1,1.2,1.3]
# for weight in list_weight:
#     for bias in list_bias:
#         coeffs = []
#         for traffic in traffics:
#             coeffs.append(bi_coef(traffic, weight = weight, bias= bias))
#         plt.plot(traffics, coeffs, label = f"{weight} - {bias}")
# plt.legend()
# plt.show()


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
                algorithm_due="fw",
                max_iter_mode_choice=max_iter_mode_choice,
                plot=True,
                return_network=True,
                CAP = False,
                capacity_field = "capacity")

plot_network(edge_df, node_df, width_col=f'flow_car',
                     color_col_num=f'flow_car', cmap='Reds',
                     title=f'Car flows', node_size=3, colorbar_label='Flow (cars)',
                     base_width=0.1, width_scale=1)
plt.show()
plot_network(edge_df, node_df, width_col=f'flow_bike',
                     color_col_num=f'flow_bike', cmap='Greens',
                     title=f'Car flows', node_size=3, colorbar_label='Flow (Bike)',
                     base_width=1, width_scale=1)
plt.show()
plot_od_matrix(updated_od_car,edge_df,node_df)
plt.show()