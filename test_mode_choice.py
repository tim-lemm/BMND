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
# beta_time = -0.000235
beta_time = parameter_dict['beta_time']
ASC_car = parameter_dict['ASC_car']
ASC_bike = parameter_dict['ASC_bike']
mu_mode = parameter_dict['mu_mode']
max_iter_mode_choice = parameter_dict['max_iter_mode_choice']
plot = False

size_od = max(node_df['id']) + 1

centre = -0.000001
pas = 0.0000001
n_valeurs = 10
debut = centre - (n_valeurs // 2) * pas
fin = debut + n_valeurs * pas
liste_beta_time = np.arange(debut, fin, pas).tolist()
liste_diff_mc_bp = []
liste_diff_mc_nbp = []

for beta_time in liste_beta_time:
    edge_df["type_bike"]="bike_path"
    edge_df = update_network(edge_df, flow_name='flow_car', free_flow_time_name='free_flow_time_car',
                             congested_time_name='travel_time_car', alpha=0.15,
                             beta=4, CAP=True)
    results_df, updated_od_car, updated_od_bike, prob_matrice_car, prob_matrice_bike, edge_df = mode_choice(edge_df,
                    node_df,
                    od_df,
                    beta_time=beta_time,
                    ASC_car=ASC_car,
                    ASC_bike=ASC_bike,
                    mu_mode=mu_mode,
                    algorithm_due="fw",
                    max_iter_mode_choice=max_iter_mode_choice,
                    plot=False,
                    return_network=True,
                    CAP = False)

    diff_mc = max(results_df["modal_share_bike"]) - min(results_df["modal_share_bike"])
    liste_diff_mc_bp.append(diff_mc)

    edge_df["type_bike"] = "None"
    edge_df = update_network(edge_df, flow_name='flow_car', free_flow_time_name='free_flow_time_car',
                             congested_time_name='travel_time_car', alpha=0.15,
                             beta=4, CAP=True)
    results_df, updated_od_car, updated_od_bike, prob_matrice_car, prob_matrice_bike, edge_df = mode_choice(edge_df,
                                                                                                            node_df,
                                                                                                            od_df,
                                                                                                            beta_time=beta_time,
                                                                                                            ASC_car=ASC_car,
                                                                                                            ASC_bike=ASC_bike,
                                                                                                            mu_mode=mu_mode,
                                                                                                            algorithm_due="fw",
                                                                                                            max_iter_mode_choice=max_iter_mode_choice,
                                                                                                            plot=False,
                                                                                                            return_network=True,
                                                                                                            CAP=False)

    diff_mc = max(results_df["modal_share_bike"]) - min(results_df["modal_share_bike"])
    liste_diff_mc_nbp.append(diff_mc)

df_calibration = pd.DataFrame({"beta_time": liste_beta_time,"diff_mc_nbp": liste_diff_mc_nbp,"diff_mc_bp": liste_diff_mc_bp})
df_calibration.plot(x='beta_time', y=['diff_mc_nbp','diff_mc_bp'], legend = True, grid = True)
plt.show()