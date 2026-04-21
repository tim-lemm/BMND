import warnings
import logging
from src.utils_sta import ta_due, ta_stochastic, plot_vc_histogram
from utils_network_processing import *
from utils_plotting import *
from utils_od_matrix_generator import generate_od_df
from utils_eaquilibrea_interface import *
from config import parameter



CURRENT_DIR = "/Users/tristan.lemoalle/Documents/Thèse/Code/code_these/"

warnings.filterwarnings('ignore')
logging.getLogger("aequilibrae").setLevel(logging.ERROR)

edge_df, node_df = import_network("data/Sioux_Falls/edges_Sioux_Falls.csv", "data/Sioux_Falls/nodes_Sioux_Falls.csv", real_network=True)
plot_network(edge_df, node_df,
             node_id_col='id',
             node_label=True,
             color_col_num='travel_time_car',
             base_width=1,
             legend=True,
             title="Network with Free Flow Time",
             figsize=(8, 8))
plt.show()

od_df_eaq = pd.read_csv("data/Sioux_Falls/SiouxFalls_od.csv")
# od_df = generate_od_df(17, od_scenario="2OD_SF", max_demand=3000)
# od_df_eaq = convert_to_eaquilibrae_od_matrix(od_df)
plot_od_matrix(od_df_eaq, edge_df, node_df)
plt.show()
#
parameter_dict = parameter()
algorithm_due = parameter_dict['ta_due_algorithm']
algorithm_sto = parameter_dict['ta_sto_algorithm']
max_iter = parameter_dict['max_iter_ta']
tolerance = parameter_dict['tolerance']
max_route = parameter_dict['max_route']
## ta_due tests

results_ta_due = ta_due(edge_df,
                        od_df_eaq,
                        algorithm="fw",
                        max_iter=max_iter,
                        tolerance=tolerance,
                        time_field='free_flow_time_car',
                        cost_field='free_flow_time_car',
                        capacity_field='capacity_cars',
                        verbose=True)

edge_df=results_ta_due['network']
plot_network(edge_df, node_df,color_col_num='flow', width_col='flow', base_width=0.1, width_scale=2, cmap="Reds", title = "Car flows")

plt.show()
plot_vc_histogram(edge_df, capacity_col='capacity_cars', bins=20)

edge_df=update_network(edge_df)
## ta_sto
results_ta_sto = ta_stochastic(edge_df,
                                od_df_eaq,
                                mode='bikes',
                                time_field='free_flow_time_bike',
                                cost_field='length_bi',
                                algorithm=algorithm_sto,
                                max_routes=max_route,
                                capacity_field='capacity_bikes',
                                verbose=True)
edge_df = results_ta_sto['network']
plot_network(edge_df, node_df,color_col_num='flow', width_col='flow', base_width=0.1, width_scale=2, cmap="Greens", title = "Bike flows")
plt.show()

edge_df["bi_coef"]=edge_df["length_bi"]/edge_df["length"]
plot_network(edge_df, node_df,
             node_id_col='id',
             node_label=True,
             color_col_num='bi_coef',
             base_width=1,
             legend=True,
             title="Network with bikeability",
             figsize=(8, 8))
plt.show()