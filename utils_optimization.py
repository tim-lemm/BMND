#TODO: termine le transfert des fonction d'optimization de test_optimization ici

import pandas as pd
from config import *
from utils_network_processing import *
from utils_plotting import *
from utils_traffic import *


def _create_empty_result_df_optimization():
    return pd.DataFrame({'iteration': [0],
                         'nbr_bike_lanes': [np.nan],
                         'nbr_none_bike_lanes': [np.nan],
                         'modal_share_car': [np.nan],
                         'modal_share_bike': [np.nan],
                         'index_removed': [np.nan],
                         'flow_of_removed_edge': [np.nan]})

def update_result_df_optimization(results_df_opt, i, nbr_bike_lanes, nbr_none_bike_lanes, modal_share_car, modal_share_bike, index_least_used, flow_of_removed_edge):
    return pd.concat([results_df_opt,pd.DataFrame({'iteration': [int(i)],
                                                   'nbr_bike_lanes': [nbr_bike_lanes],
                                                   'nbr_none_bike_lanes': [nbr_none_bike_lanes],
                                                   'modal_share_car': [modal_share_car],
                                                   'modal_share_bike':[modal_share_bike],
                                                   'index_removed': [index_least_used],
                                                   'flow_of_removed_edge': [flow_of_removed_edge]})],
                     ignore_index=True)

def reverse_growth_optimization(edge_df, node_df, od_df, limit:int = 48, plot = False, od_shape = 'squared', nbr_removal = 1):
    # construct bike lane on all edge
    edge_df = apply_bike_infra_scenario(edge_df, 2)

    # parameters for mode choice
    parameter_dict = parameter()
    beta_time = parameter_dict['beta_time']
    ASC_car = parameter_dict['ASC_car']
    ASC_bike = parameter_dict['ASC_bike']
    mu_mode = parameter_dict['mu_mode']
    max_iter_mode_choice = parameter_dict['max_iter_mode_choice']

    i = 0

    nbr_bike_lanes = edge_df['type_bike'].notnull().sum()
    nbr_none_bike_lanes = edge_df['type_bike'].isnull().sum()

    results_df_opt = _create_empty_result_df_optimization()
    results_df_opt.loc[0, "nbr_bike_lanes"] = nbr_bike_lanes
    results_df_opt.loc[0, "nbr_none_bike_lanes"] = nbr_none_bike_lanes
    print(f"Initial number of bike infrastructures: {nbr_bike_lanes}")

    edge_df_results = edge_df.copy()
    edge_df_results.drop(['travel_time_car', 'travel_time_bike', 'flow_car', 'flow_bike', 'length_bi'], axis=1,
                         inplace=True)

    while nbr_bike_lanes > 0 and i < limit:

        print(f"\n--- Iteration {i} ---")

        # mode choice
        print("➡️ Running mode choice...")
        results_df, updated_od_car, updated_od_bike, prob_matrice_car, prob_matrice_bike, edge_df = mode_choice(edge_df,
                                                                                                                node_df,
                                                                                                                od_df,
                                                                                                                beta_time,
                                                                                                                ASC_car,
                                                                                                                ASC_bike,
                                                                                                                mu_mode=mu_mode,
                                                                                                                max_iter_mode_choice=max_iter_mode_choice,
                                                                                                                plot=plot,
                                                                                                                od_shape=od_shape,
                                                                                                                return_network=True)

        # update edge_df_results
        name_col_flow_car = 'flow_car_iteration_' + str(i)
        name_col_flow_bike = 'flow_bike_iteration_' + str(i)
        name_col_tt_car = 'travel_time_car_' + str(i)
        name_col_tt_bike = 'travel_time_bike_' + str(i)

        cols_to_transfer = ['id', 'flow_car', 'flow_bike', 'travel_time_car', 'travel_time_bike']
        edge_df_results = edge_df_results.merge(
            edge_df[cols_to_transfer],
            on='id',
            how='left'
        )
        edge_df_results = edge_df_results.rename(columns={
            'flow_car': name_col_flow_car,
            'flow_bike': name_col_flow_bike,
            'travel_time_car': name_col_tt_car,
            'travel_time_bike': name_col_tt_bike
        })

        # identify edges considered for removal
        edges_considered_for_removal = edge_df_results[edge_df_results['type_bike'] != "None"]
        #remove all edges with no flow
        index_with_no_flow = edges_considered_for_removal[edges_considered_for_removal[name_col_flow_bike] < 1]["id"].values.tolist()
        edge_df_results.loc[edge_df_results['id'].isin(index_with_no_flow), 'type_bike'] = "None"
        edge_df.loc[edge_df['id'].isin(index_with_no_flow), 'type_bike'] = "None"
        print(f"Iteration {i} - Removing bike lane on edge {index_with_no_flow} with no flow")
        nbr_removed_bike_lanes = len(index_with_no_flow)

        # identify edges considered for removal
        edges_considered_for_removal = edge_df_results[edge_df_results['type_bike'] != "None"]
        # select index of the nbr_removal least used edge
        # Sort the DataFrame first, then pull the 'id' column
        index_least_used = edges_considered_for_removal.sort_values(by=name_col_flow_bike, ascending=True)["id"].tolist()[:nbr_removal - 1]
        avg_flow_removed = edge_df_results.loc[edge_df_results['id'].isin(index_least_used), name_col_flow_bike].mean()
        nbr_removed_bike_lanes += len(index_least_used)
        # remove infrastructures from selected edges
        edge_df.loc[edge_df['id'].isin(index_least_used), 'type_bike'] = "None"
        edge_df_results.loc[edge_df_results['id'].isin(index_least_used), 'type_bike'] = "None"
        print(f"Iteration {i} - Removing bike lane on edge {index_least_used} with average flow of {avg_flow_removed}")

        if plot:
            plot_network(edge_df, node_df, color_col_str='type_bike', base_width=1, width_scale=5, node_size=200,
                         legend=True,
                         node_label=True, title=f'Bike Infrastructure on iteration {i}')
            plt.show()

        # update results_df_opt
        list_index_removed = index_with_no_flow + index_least_used
        nbr_bike_lanes = nbr_bike_lanes - nbr_removed_bike_lanes
        nbr_none_bike_lanes = nbr_none_bike_lanes + nbr_removed_bike_lanes
        modal_share_car = results_df["modal_share_car"].iloc[-1]
        modal_share_bike = results_df["modal_share_bike"].iloc[-1]
        results_df_opt = update_result_df_optimization(results_df_opt, i, nbr_bike_lanes, nbr_none_bike_lanes,
                                                       modal_share_car, modal_share_bike, list_index_removed,
                                                       avg_flow_removed)
        i += 1
    return edge_df_results, results_df_opt