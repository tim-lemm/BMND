import warnings
import logging
from utils_traffic import *
from utils_network_processing import *
from utils_plotting import *
from utils_od_matrix_generator import generate_od_df
from config import parameter

#TODO: update readme



warnings.filterwarnings('ignore')
logging.getLogger("aequilibrae").setLevel(logging.ERROR)

edge_df = pd.read_csv("data/Delft/edges.csv")
edge_df = initialization_delft(edge_df)
node_df = pd.read_csv("data/Delft/nodes.csv")
od_df = pd.read_csv("data/Delft/od.csv")
# od_df['demand'] *= 10
# parameters for mode choice
parameter_dict = parameter()
beta_time = parameter_dict['beta_time']
ASC_car = parameter_dict['ASC_car']
ASC_bike = parameter_dict['ASC_bike']
mu_mode = parameter_dict['mu_mode']
max_iter_mode_choice = parameter_dict['max_iter_mode_choice']+5
plot = True
#beta_time = -1.354e-8
step = 1e-13
n_points = 5
#list_beta_time = [beta_time - (i * step) for i in range(n_points + 1)]
list_beta_time = [beta_time]
fig, ax = plt.subplots(1,2, figsize=(15,5))

for beta_time in list_beta_time:
    edge_df = apply_bike_infra_scenario(edge_df, 0)
    #edge_df.loc[edge_df["road_type"] < 5, "type_bike"] = "bike_path"
    # plot_network(edge_df, node_df, node_id_col='id',
    #                      node_label=False,
    #                      color_col_str='type_bike',
    #                      base_width=1,
    #                      legend=True,
    #              node_size=0,
    #                      title=f"Network ")

    result_df,_,_,_,_, edge_df_results = mode_choice(edge_df,
                                      node_df,
                                      od_df,
                                      beta_time,
                                      ASC_car,
                                      ASC_bike,
                                      mu_mode=mu_mode,
                                      max_iter_mode_choice=max_iter_mode_choice,
                                      plot=plot,
                                      od_shape="long",
                                    return_network=True)
    result_df.plot(x="iteration",y="modal_share_bike", label=beta_time,ax=ax[0])
    result_df.plot(x="iteration",y="total_travel_time_bike",ax=ax[1])
ax[0].set_xlabel("Iteration")
ax[0].set_ylabel("Modal Share Bike")
ax[0].legend()
ax[0].set_title("Modal Share Bike")
ax[0].grid(True)
ax[1].set_xlabel("Iteration")
ax[1].set_ylabel("TTT Bike")
ax[1].set_title("TTT Bike")
ax[1].legend([])
ax[1].grid(True)
plt.show()

# edge_df_results["coef_bi"]=edge_df_results["length_bi"]/edge_df_results["length"]
#
# fig, axes = plt.subplots(1,3, figsize=(30,10))
# plot_network(edge_df_results, node_df, width_col='flow_car', color_col_num='flow_car', cmap='Reds',
#                  title=f'Delft - Car flows', node_size=3, colorbar_label='Flow (cars)',
#                  base_width=0.1, width_scale=10, ax=axes[0])
# plot_network(edge_df_results, node_df,node_label=False,color_col_num='coef_bi', base_width=1, title=f"Delft with coef_bi",node_size=15, ax=axes[1],cmap="summer_r")
# plot_network(edge_df_results, node_df, width_col='flow_bike', color_col_num='flow_bike', cmap='Greens',
#              title=f'Delft - Bike flows', node_size=3, colorbar_label='Flow (bikes)',
#              base_width=0.1, width_scale=10, ax=axes[2])
# plt.show()
