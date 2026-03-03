import warnings
import logging

import matplotlib.pyplot as plt

from traffic import *
from network_processing import *
from plotting import *
from od_matrix_generator import generate_od_df
from config import parameter
import seaborn as sns

#TODO: update readme

CURRENT_DIR = ""

warnings.filterwarnings('ignore')
logging.getLogger("aequilibrae").setLevel(logging.ERROR)

edge_df, node_df = import_network(CURRENT_DIR + "data/edges_small_grid_2.csv", CURRENT_DIR + "data/nodes_small_grid_2.csv")

plot_network(edge_df, node_df,
             node_id_col='node',
             node_label=True,
             color_col_str='type_bike',
             base_width=1,
             legend=False,
             title="Network",
             figsize=(8, 8))

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

result_df, updated_od_car, updated_od_bike,prob_matrice_car, prob_matrice_bike = mode_choice(edge_df,
                                                                                            node_df,
                                                                                             od_df,
                                                                                             beta_time,
                                                                                             ASC_car,
                                                                                             ASC_bike,
                                                                                             mu_mode=mu_mode,
                                                                                             max_iter_mode_choice=10,
                                                                                             plot=plot)

np.fill_diagonal(prob_matrice_car, np.nan)
np.fill_diagonal(prob_matrice_bike, np.nan)
values_car = prob_matrice_car[1:,1:].flatten()
values_bike = prob_matrice_bike[1:,1:].flatten()
values_car = values_car[~np.isnan(values_car)]
values_bike = values_bike[~np.isnan(values_bike)]
mean_car = np.mean(values_car)
mean_bike = np.mean(values_bike)

plt.figure(figsize=(8, 8))
sns.histplot(values_car, label='car',bins=20, stat='count')
plt.vlines(mean_car, 0, 40, linestyle='dashed', label='mean car')
plt.legend()
plt.grid(True)
plt.title(f"Distribution of probability for every OD pair for cars")
plt.show()


plt.figure(figsize=(8, 8))
sns.histplot(values_bike, label='bike', bins=20, stat='count', color='orange')
plt.vlines(mean_bike, 0, 40,colors="orange", linestyle='dashed', label='mean bike')
plt.legend()
plt.grid(True)
plt.title(f"Distribution of probability for every OD pair for bikes")
plt.show()

liste_nodes = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
for a_node in liste_nodes:
    for b_node in liste_nodes:
        edge_df = change_type_infra(edge_df,a_node,b_node,"bike_path")
# edge_df = change_type_infra(edge_df,1,2,"bike_path")
# edge_df = change_type_infra(edge_df,2,1,"bike_path")
# edge_df = change_type_infra(edge_df,2,3,"bike_path")
# edge_df = change_type_infra(edge_df,3,2,"bike_path")
# edge_df = change_type_infra(edge_df,3,4,"bike_path")
# edge_df = change_type_infra(edge_df,4,3,"bike_path")
# edge_df = change_type_infra(edge_df,13,14,"bike_path")
# edge_df = change_type_infra(edge_df,14,15,"bike_path")
# edge_df = change_type_infra(edge_df,15,16,"bike_path")

plot_network(edge_df, node_df,
             node_id_col='node',
             node_label=True,
             color_col_str='type_bike',
             base_width=1,
             legend=False,
             title="Network",
             figsize=(8, 8))

result_df, updated_od_car, updated_od_bike,prob_matrice_car, prob_matrice_bike = mode_choice(edge_df,
                                                                                            node_df,
                                                                                             od_df,
                                                                                             beta_time,
                                                                                             ASC_car,
                                                                                             ASC_bike,
                                                                                             mu_mode=mu_mode,
                                                                                             max_iter_mode_choice=10,
                                                                                             plot=plot)

np.fill_diagonal(prob_matrice_car, np.nan)
np.fill_diagonal(prob_matrice_bike, np.nan)
values_car = prob_matrice_car[1:,1:].flatten()
values_bike = prob_matrice_bike[1:,1:].flatten()
values_car = values_car[~np.isnan(values_car)]
values_bike = values_bike[~np.isnan(values_bike)]
mean_car = np.mean(values_car)
mean_bike = np.mean(values_bike)

print(mean_car)
print(mean_bike)


plt.figure(figsize=(8, 8))
sns.histplot(values_car, label='car',bins=20, stat='count')
plt.vlines(mean_car, 0, 40, linestyle='dashed', label='mean car')
plt.legend()
plt.grid(True)
plt.title(f"Distribution of probability for every OD pair for cars")
plt.show()


plt.figure(figsize=(8, 8))
sns.histplot(values_bike, label='bike', bins=20, stat='count', color='orange')
plt.vlines(mean_bike, 0, 40,colors="orange", linestyle='dashed', label='mean bike')
plt.legend()
plt.grid(True)
plt.title(f"Distribution of probability for every OD pair for bikes")
plt.show()