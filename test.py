import matplotlib.pyplot as plt
import pandas as pd
plt.rcParams.update({'font.size': 20})

from utils_network_processing import *
from utils_plotting import *

city_name = "Sioux_Falls"
name_test = f"CAP_{city_name}_test_-0.001_-2_bi_11"
horodatage = "2026-08-25_11-07-44"
edge_df, node_df = import_network(f"data/{city_name}/edges_{city_name}.csv", f"data/{city_name}/nodes_{city_name}.csv", real_network=True)
edge_df['existing_bike_infra']=False
edge_df['type_bike']=None
filename_results=f"output/optimization/test_parametres/{horodatage}/rgo_results_df_opt_{name_test}.csv"
filename_edge = f"output/optimization/test_parametres/{horodatage}/rgo_edge_df_results_{name_test}.csv"
results_df_opt = pd.read_csv(filename_results)
edge_df_results = pd.read_csv(filename_edge)

somme_voiture_1 = edge_df_results['flow_car_iteration_1'].sum()
somme_voiture_70 = edge_df_results['flow_car_iteration_70'].sum()
change_voiture = 100 - (somme_voiture_1/somme_voiture_70)*100
somme_velo_1 = edge_df_results['flow_bike_iteration_1'].sum()
somme_velo_70 = edge_df_results['flow_bike_iteration_70'].sum()
change_velo = 100 - (somme_velo_1/somme_velo_70)*100
print(f"Total flow of cars at iteration 1 : {somme_voiture_1}")
print(f"Total flow of cars at iteration 70 : {somme_voiture_70}, ({change_voiture} %)")
print(f"Total flow of bike at iteration 1 : {somme_velo_1}")
print(f"Total flow of cars at iteration 70 : {somme_velo_70}, ({change_velo} %)")

plot_two_iterations(1,70, node_df, edge_df_results, results_df_opt, plot_type="bike_network")
plot_two_iterations(1, 70, node_df, edge_df_results, results_df_opt, plot_type="bike_flow")
plot_two_iterations(1, 70, node_df, edge_df_results, results_df_opt, plot_type="car_flow")
plot_two_iterations(1, 70, node_df, edge_df_results, results_df_opt, plot_type="coef_bi")