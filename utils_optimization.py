

import pandas as pd
from config import *
from utils_network_processing import *
from utils_plotting import *
from utils_traffic import *
import random

def _create_empty_result_df_optimization():
    return pd.DataFrame({'iteration': [0],
                         'nbr_bike_lanes': [np.nan],
                         'nbr_none_bike_lanes': [np.nan],
                         'modal_share_car': [np.nan],
                         'modal_share_bike': [np.nan],
                         'index_removed': [np.nan],
                         'flow_of_removed_edge': [np.nan],
                         'average_bi_coef':[np.nan]})

def update_result_df_optimization(results_df_opt, i, nbr_bike_lanes, nbr_none_bike_lanes, modal_share_car, modal_share_bike, index_least_used, flow_of_removed_edge, average_bi_coef):
    return pd.concat([results_df_opt,pd.DataFrame({'iteration': [int(i)],
                                                   'nbr_bike_lanes': [nbr_bike_lanes],
                                                   'nbr_none_bike_lanes': [nbr_none_bike_lanes],
                                                   'modal_share_car': [modal_share_car],
                                                   'modal_share_bike':[modal_share_bike],
                                                   'index_removed': [index_least_used],
                                                   'flow_of_removed_edge': [flow_of_removed_edge],
                                                   'average_bi_coef': [average_bi_coef]})],
                     ignore_index=True)


def reverse_growth_optimization(edge_df, node_df, od_df, limit:int = 48, plot:bool = False, nbr_removal:int = 1, CAP:bool = True, custom_parameter_dict:dict = None):
    # construct bike lane on all edge
    edge_df = apply_bike_infra_scenario(edge_df, 2)
    if custom_parameter_dict is None:
        # parameters for mode choice
        parameter_dict = parameter()
        beta_time = parameter_dict['beta_time']
        ASC_car = parameter_dict['ASC_car']
        ASC_bike = parameter_dict['ASC_bike']
        mu_mode = parameter_dict['mu_mode']
        max_iter_mode_choice = parameter_dict['max_iter_mode_choice']
    else:
        beta_time = custom_parameter_dict['beta_time']
        ASC_car = custom_parameter_dict['ASC_car']
        ASC_bike = custom_parameter_dict['ASC_bike']
        mu_mode = custom_parameter_dict['mu_mode']
        max_iter_mode_choice = custom_parameter_dict['max_iter_mode_choice']
        speed_bike = custom_parameter_dict['speed_bike']
        edge_df["speed_bike"] = speed_bike/3.6
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
                                                                                                                return_network=True,
                                                                                                                CAP=CAP)

        edge_df["coef_bi"] = edge_df["length_bi"] / edge_df["length"]
        # update edge_df_results
        name_col_flow_car = 'flow_car_iteration_' + str(i)
        name_col_flow_bike = 'flow_bike_iteration_' + str(i)
        name_col_tt_car = 'travel_time_car_' + str(i)
        name_col_tt_bike = 'travel_time_bike_' + str(i)
        name_col_coef_bi = 'coef_bi_' + str(i)

        cols_to_transfer = ['id', 'flow_car', 'flow_bike', 'travel_time_car', 'travel_time_bike', "coef_bi"]
        edge_df_results = edge_df_results.merge(
            edge_df[cols_to_transfer],
            on='id',
            how='left'
        )
        edge_df_results = edge_df_results.rename(columns={
            'flow_car': name_col_flow_car,
            'flow_bike': name_col_flow_bike,
            'travel_time_car': name_col_tt_car,
            'travel_time_bike': name_col_tt_bike,
            'coef_bi': name_col_coef_bi
        })
        # identify edges considered for removal
        edges_considered_for_removal = edge_df_results[edge_df_results['type_bike'] != "None"]
        # select index of least used edge
        index_least_used = edges_considered_for_removal.sort_values(by=name_col_flow_bike, ascending=True)["id"].tolist()[:nbr_removal]
        flow_of_removed_edge = edge_df_results.loc[edge_df_results['id'].isin(index_least_used), name_col_flow_bike].mean()

        # remove infrastructures from selected edges
        print(f"Iteration {i} - Removing bike lane on edge {index_least_used} with flow {flow_of_removed_edge}")
        edge_df.loc[edge_df['id'].isin(index_least_used), 'type_bike'] = "None"
        edge_df_results.loc[edge_df_results['id'].isin(index_least_used), 'type_bike'] = "None"
        if plot:
            plot_network(edge_df, node_df, color_col_str='type_bike', base_width=1, width_scale=5, node_size=200,
                         legend=True,
                         node_label=True, title=f'Bike Infrastructure on iteration {i}')
            plt.show()

        # update results_df_opt
        nbr_bike_lanes = nbr_bike_lanes - 1
        nbr_none_bike_lanes = nbr_none_bike_lanes + 1
        modal_share_car = results_df["modal_share_car"].iloc[-1]
        modal_share_bike = results_df["modal_share_bike"].iloc[-1]
        average_bi_coef = edge_df['coef_bi'].mean()
        results_df_opt = update_result_df_optimization(results_df_opt, i, nbr_bike_lanes, nbr_none_bike_lanes,modal_share_car, modal_share_bike, index_least_used,
                                                       flow_of_removed_edge, average_bi_coef)

        i += 1
    return edge_df_results, results_df_opt

def test_random(edge_df, node_df, od_df, CAP:bool = True):
    parameter_dict = parameter()
    beta_time = parameter_dict['beta_time']
    ASC_car = parameter_dict['ASC_car']
    ASC_bike = parameter_dict['ASC_bike']
    mu_mode = parameter_dict['mu_mode']
    max_iter_mode_choice = parameter_dict['max_iter_mode_choice']

    list_modal_share = []
    list_tt_bike = []
    list_tt_car = []
    list_seed = random.sample(range(1, 10000000000000), 100)
    list_edge = edge_df["id"]

    for seed in list_seed:
        random.seed(seed)
        list_random_edges = random.sample(list_edge.tolist(), 10)
        edge_df = change_type_bike_infra_with_index(edge_df, 'bike_path', list_random_edges)

        result_df, _, _, _, _ = mode_choice(
            edge_df,
            node_df,
            od_df,
            beta_time,
            ASC_car,
            ASC_bike,
            mu_mode=mu_mode,
            max_iter_mode_choice=max_iter_mode_choice,
            plot=False,
            CAP=CAP)
        result_df.head()
        modal_share_bike = result_df['modal_share_bike'].iloc[-1]
        tt_bike = result_df['total_travel_time_bike'].iloc[-1]
        tt_car = result_df['total_travel_time_car'].iloc[-1]
        list_modal_share.append(modal_share_bike)
        list_tt_bike.append(tt_bike)
        list_tt_car.append(tt_car)
        edge_df = apply_bike_infra_scenario(edge_df, 0)
    results_test_random_df = pd.DataFrame({
        'seed': list_seed,
        'modal_share_bike': list_modal_share,
        'travel_time_bike': list_tt_bike,
        'travel_time_car': list_tt_car,
        })
    return results_test_random_df