import matplotlib.pyplot as plt
from matplotlib.pyplot import legend
from utils_network_processing import *
from utils_plotting import *
plt.rcParams.update({'font.size': 30})
import os
from PIL import Image




total_lanes = 75  # Remplacez cette valeur par le total réel de votre réseau
city_name = "Sioux_Falls"
horodatage = "2026-10-07_17-48-00"
beta_time = -0.001
ASC_bike = -2
list_metric_of_selection = ["flow_bike","betweenness_centrality","betweenness_centrality_weighted"]
list_metric_to_plot = ["modal_share_bike",
                       "average_bi_coef",
                       "betweenness_centrality_of_removed_edge",
                       "betweenness_centrality_weighted_of_removed_edge"]
fig, axes = plt.subplots(len(list_metric_to_plot), 1, figsize=(25, 10*len(list_metric_to_plot)))
coef_map_num = 31

for metric in list_metric_of_selection:
    name_test = f"CAP_{city_name}_test_{beta_time}_{ASC_bike}_bi_{coef_map_num}_{metric}"
    filename = f"output/optimization/test_parametres/{horodatage}/rgo_results_df_opt_{name_test}.csv"
    df = pd.read_csv(filename)

    # Conversion du nombre de pistes en pourcentage
    df["pct_bike_lanes"] = (df["nbr_bike_lanes"] / total_lanes) * 100
    for i, plot_metric in enumerate(list_metric_to_plot):
        if plot_metric.removesuffix("_of_removed_edge") == metric or plot_metric == "modal_share_bike" or plot_metric == "average_bi_coef":
            axes[i].plot(df["pct_bike_lanes"], df[plot_metric], linewidth=3, label=metric)
        else :
            axes[i].plot(df["pct_bike_lanes"], df[plot_metric], linewidth=2, label=metric, linestyle="dashdot")

for i, plot_metric in enumerate(list_metric_to_plot):
    axes[i].set_ylabel(plot_metric)
# Configuration des axes
for ax in axes:
    ax.set_xlabel("Percentage of dedicated bike lanes (%)")
    ax.grid(True, alpha=0.3)
    ax.legend()


os.makedirs(f"output/optimization/test_parametres/{horodatage}/images", exist_ok=True)
plt.show()


for metric in list_metric_of_selection:
    edge_df, node_df = import_network(f"data/{city_name}/edges_{city_name}.csv",
                                      f"data/{city_name}/nodes_{city_name}.csv", real_network=True)
    edge_df['existing_bike_infra'] = False
    edge_df['type_bike'] = None
    name_test = f"CAP_{city_name}_test_{beta_time}_{ASC_bike}_bi_{coef_map_num}_{metric}"
    edge_df_results_filename = f"output/optimization/test_parametres/{horodatage}/rgo_edge_df_results_{name_test}.csv"
    df_opt_filename = f"output/optimization/test_parametres/{horodatage}/rgo_results_df_opt_{name_test}.csv"
    edge_df_results = pd.read_csv(edge_df_results_filename)
    results_df_opt = pd.read_csv(df_opt_filename)

    results_df_opt.drop("Unnamed: 0", axis=1, inplace=True)
    results_df_opt = results_df_opt.iloc[1:].reset_index(drop=True)
    results_df_opt["index_removed"] = results_df_opt["index_removed"].apply(ast.literal_eval)
    results_df_opt = results_df_opt.explode('index_removed')


    edge_df = edge_df.merge(results_df_opt, how="inner", left_on="id", right_on="index_removed")
    edge_df.index = edge_df["id"]
    edge_df.drop(
            ["nbr_bike_lanes", "nbr_none_bike_lanes", "modal_share_car", "modal_share_bike",
             "index_removed",
             "flow_of_removed_edge"], axis=1, inplace=True)
    edge_df.rename(columns={'iteration': 'iteration_of_removal'}, inplace=True)
    fig, ax = plt.subplots(1, 1, figsize=(15, 15))
    plot_network(edge_df, node_df, node_id_col='id',
                         node_label=False,
                         color_col_num='iteration_of_removal',
                         base_width=1,
                         legend=True,
                         title=metric,
                 cmap="magma",
                     ax=ax, show_nodes=True, colorbar_label = "(<-- Low) Edge importance in the bike network (High -->)")
    plt.savefig(f"output/optimization/test_parametres/{horodatage}/images/network_{metric}.png")