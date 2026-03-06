import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from shapely.geometry import Polygon
import pandas as pd
from utils_network_processing import *
from pathlib import Path


#### plotting functions
def _create_offset_polygon(coords, width):
    """Create polygon offset to right of line. From utils_traffic.py by Bahman"""
    if len(coords) < 2:
        return None

    right_pts, left_pts = [], []
    for i, (cx, cy) in enumerate(coords):
        if i == 0:
            dx, dy = coords[1][0] - coords[0][0], coords[1][1] - coords[0][1]
        elif i == len(coords) - 1:
            dx, dy = coords[-1][0] - coords[-2][0], coords[-1][1] - coords[-2][1]
        else:
            dx = (coords[i + 1][0] - coords[i - 1][0]) / 2
            dy = (coords[i + 1][1] - coords[i - 1][1]) / 2

        length = np.sqrt(dx ** 2 + dy ** 2)
        if length > 0:
            dx, dy = dx / length, dy / length

        perp_x, perp_y = dy, -dx
        right_pts.append((cx + perp_x * width, cy + perp_y * width))
        left_pts.append((cx, cy))

    try:
        polygon = Polygon(right_pts + left_pts[::-1])
        return polygon if polygon.is_valid else polygon.buffer(0)
    except:
        return None


def plot_network(edges_df, nodes_df, ax=None, figsize=(10, 10), node_x_col='x', node_y_col='y',
                 width_col=None, base_width=0.1, width_scale=2.1, node_id_col='node', color_col_num=None,
                 color_col_str=None, dict_colors_str=None,
                 vmin=None, vmax=None, a_node_col='a_node', b_node_col='b_node', show_nodes=True,
                 node_size=100, cmap='viridis', colorbar_label=None, title=None, node_label=False, legend=False,
                 edges_label_col=None):
    """ Plot a network with edge widths and colors based on specified columns. Adapted from utils_traffic.py by Bahman """

    edges_df = edges_df.reset_index(drop=True)

    if dict_colors_str is not None:
        dict_colors = dict_colors_str
    else:
        dict_colors = {'bike_path': '#4E9F50FF', 'bike_lane': '#EF8A0CFF', 'none': 'black'}
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    x_range = nodes_df[node_x_col].max() - nodes_df[node_x_col].min()
    y_range = nodes_df[node_y_col].max() - nodes_df[node_y_col].min()
    scale = min(x_range, y_range) / 100

    scaled_base = scale * base_width
    scaled_scale = scale * width_scale * 0.0001

    node_coords = {r[node_id_col]: (r[node_x_col], r[node_y_col])
                   for _, r in nodes_df.iterrows()}

    if width_col is not None:
        width_vals = edges_df[width_col].fillna(0).values if width_col in edges_df.columns else np.ones(len(edges_df))
        if color_col_num is None:
            color_col_num = width_col

    if color_col_num in edges_df.columns:
        color_vals = edges_df[color_col_num].fillna(0).values

        # Use provided vmin/vmax or compute from data
        if vmin is None:
            vmin = np.nanmin(color_vals)
        if vmax is None:
            vmax = np.nanmax(color_vals)
        if vmin == vmax:
            vmax = vmin + 1

        norm = plt.Normalize(vmin, vmax)
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        use_cmap = True
    else:
        use_cmap = False

    if color_col_str in edges_df.columns:
        color_vals = []
        for edge in edges_df.itertuples():
            color_vals.append(dict_colors.get(getattr(edge, color_col_str), 'black'))
        use_cmap = False

    if color_col_num is None and color_col_str is None:
        color_vals = ['black'] * len(edges_df)
        use_cmap = False

    # Use enumerate to get integer index for numpy array access
    for idx, edge in edges_df.iterrows():
        a_coords = node_coords.get(edge[a_node_col])
        b_coords = node_coords.get(edge[b_node_col])
        if a_coords is None or b_coords is None:
            continue

        # Use idx (which is now 0..N-1 due to reset_index) to access arrays
        if width_col is not None:
            width = scaled_base + width_vals[idx] * scaled_scale
        else:
            width = scaled_base
        polygon = _create_offset_polygon([a_coords, b_coords], width)

        if polygon:
            color = sm.to_rgba(color_vals[idx]) if use_cmap else color_vals[idx]
            x, y = polygon.exterior.xy
            ax.fill(x, y, color=color, alpha=1, edgecolor='black', linewidth=0.1)

    if show_nodes:
        ax.scatter(nodes_df[node_x_col], nodes_df[node_y_col], s=node_size, c='white', zorder=5, edgecolors='black')
        if node_label:
            for _, row in nodes_df.iterrows():
                ax.text(row[node_x_col], row[node_y_col], str(int(row[node_id_col])), fontsize=8,
                        ha='center', va='center', zorder=6)

    if legend and color_col_str is not None:
        legend_elements = []
        for key, color in dict_colors.items():
            legend_elements.append(Line2D([0], [0], color=color, lw=4, label=key))
        ax.legend(handles=legend_elements, loc='lower right')

    if use_cmap:
        # Determine colorbar label
        if colorbar_label is None:
            colorbar_label = color_col_num.replace('_', ' ').title()
        cbar = plt.colorbar(sm, ax=ax, label=colorbar_label, shrink=0.8)

    if edges_label_col is not None and edges_label_col in edges_df.columns:
        for _, edge in edges_df.iterrows():
            a_coords = node_coords.get(edge[a_node_col])
            b_coords = node_coords.get(edge[b_node_col])
            if a_coords is None or b_coords is None:
                continue
            mid_x = (a_coords[0] + b_coords[0]) / 2
            mid_y = (a_coords[1] + b_coords[1]) / 2
            if a_coords[0] == b_coords[0]:  # horizontal line
                ax.text(mid_x, mid_y, str(edge[edges_label_col]), fontsize=10,
                        ha='center', va='center', zorder=6, color='black', backgroundcolor='white', rotation='vertical')
            else:  # vertical line
                ax.text(mid_x, mid_y, str(edge[edges_label_col]), fontsize=10,
                        ha='center', va='center', zorder=6, color='black', backgroundcolor='white')

    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title or f'Network (width by {width_col})')
    plt.tight_layout()
    if ax is None:
        return fig, ax


def plot_od_matrix(od_matrix, edges_df, nodes_df, ax=None, figsize=(10, 10), cmap='viridis', title='OD Matrix',
                   label=False, color='red', vmax=None):
    """ Plot OD matrix as arrows on the network."""
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    plot_network(edges_df, nodes_df, ax=ax, show_nodes=True, node_label=True, node_size=300, title=title)
    od_matrix_plot = od_matrix.copy()[od_matrix['demand'] > 0]
    if vmax is None:
        od_matrix_plot['linewidth'] = od_matrix_plot['demand'] / od_matrix_plot['demand'].max() * 5
    else:
        od_matrix_plot['linewidth'] = od_matrix_plot['demand'] / vmax * 5

    for i, row in od_matrix_plot.iterrows():
        x0 = nodes_df.loc[nodes_df['node'] == row['origin'], 'x'].values[0]
        y0 = nodes_df.loc[nodes_df['node'] == row['origin'], 'y'].values[0]
        x1 = nodes_df.loc[nodes_df['node'] == row['destination'], 'x'].values[0]
        y1 = nodes_df.loc[nodes_df['node'] == row['destination'], 'y'].values[0]

        ax.annotate(
            "",
            xy=(x1, y1),  # destination
            xytext=(x0, y0),  # origine
            arrowprops=dict(
                arrowstyle="->",
                color=color,
                lw=row['linewidth']
            ),
            zorder=3
        )
        if label:
            xm = (x0 + x1 - 100) / 2
            ym = (y0 + y1 + 100) / 2
            dx = x1 - x0
            dy = y1 - y0

            # Vecteur perpendiculaire unitaire
            nx = -dy
            ny = dx
            norm = np.sqrt(nx ** 2 + ny ** 2)
            nx /= norm
            ny /= norm

            # Distance du décalage (à ajuster si besoin)
            offset = 0.015 * np.hypot(dx, dy)

            # Position finale du texte
            xt = xm + nx * offset
            yt = ym + ny * offset

            # Texte
            ax.text(
                xt, yt,
                str(int(row['demand'])),
                color='black',
                fontsize=9,
                ha='center',
                va='center',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.7),
                zorder=4
            )

    if ax is None:
        return fig, ax

def plot_optimization_network(edge_df, edge_df_results, node_df, budget, save, output_dir_infra, output_dir_network, test_name):
    max_budget = max(edge_df["iteration_of_removal"])
    iteration_corresponding_to_budget = max_budget - budget + 1

    mask = edge_df["iteration_of_removal"] >= iteration_corresponding_to_budget
    list_index_of_bike_infra = edge_df.index[mask].tolist()

    edge_df = change_type_bike_infra_with_index(edge_df, "bike_path", list_index_of_bike_infra)
    plot_network(edge_df, node_df, node_id_col='node',
                     node_label=True,
                     color_col_str='type_bike',
                     base_width=1,
                     legend=True,
                     title=f"Network for a budget of {budget}")
    if save:
        file_path = output_dir_infra / f"infra_budget_{budget}_{test_name}.png"
        plt.savefig(file_path)
    else:
        plt.show()

    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    plot_network(edge_df_results, node_df, width_col=f'flow_car_iteration_{iteration_corresponding_to_budget}',
                     color_col_num=f'flow_car_iteration_{iteration_corresponding_to_budget}', cmap='Reds',
                     title=f'Car flows - budget: {budget}', node_size=3, colorbar_label='Flow (cars)',
                     base_width=0.1, width_scale=10, ax=axes[0, 0])
    plot_network(edge_df_results, node_df, width_col=f'flow_bike_iteration_{iteration_corresponding_to_budget}',
                     color_col_num=f'flow_bike_iteration_{iteration_corresponding_to_budget}', cmap='Greens',
                     title=f'Bike flows - budget: {budget}', node_size=3, colorbar_label='Flow (bikes)',
                     base_width=0.1, width_scale=10, ax=axes[0, 1])
    plot_network(edge_df_results, node_df, color_col_num=f'travel_time_car_{iteration_corresponding_to_budget}',
                     cmap='hot_r', title=f'Car Travel Time',
                     node_size=3, colorbar_label='Travel Time (s)', base_width=1, ax=axes[1, 0])
    plot_network(edge_df_results, node_df, color_col_num=f'travel_time_bike_{iteration_corresponding_to_budget}',
                     cmap='hot_r', title=f'Bike Travel Time',
                     node_size=3, colorbar_label='Travel Time (s)', base_width=1, ax=axes[1, 1])
    if save:
        file_path = output_dir_network / f"networks_budget_{budget}_{test_name}.png"
        plt.savefig(file_path)
    else:
        plt.show()

def plot_optimization_results(test_name:str, edge_df, node_df, save = False):
    output_dir = Path(f"output/optimization/images/{test_name}")
    output_dir_network = output_dir / "network"
    output_dir_infra = output_dir / "infrastructure"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_dir_infra.mkdir(parents=True, exist_ok=True)
    output_dir_network.mkdir(parents=True, exist_ok=True)
    edge_df_results = pd.read_csv(f"output/optimization/rgo_edge_df_results_{test_name}.csv")
    results_df_opt = pd.read_csv(f"output/optimization/rgo_results_df_opt_{test_name}.csv")

    edge_df = edge_df.merge(results_df_opt, how="inner", left_index=True, right_on="index_removed").set_index(
        edge_df.index)

    edge_df.drop(
        ["Unnamed: 0", "nbr_bike_lanes", "nbr_none_bike_lanes", "modal_share_car", "modal_share_bike", "index_removed",
         "flow_of_removed_edge"], axis=1, inplace=True)
    edge_df.rename(columns={'iteration': 'iteration_of_removal'}, inplace=True)

    plot_network(edge_df, node_df, node_id_col='node',
                     node_label=True,
                     color_col_num='iteration_of_removal',
                     base_width=1,
                     legend=True,
                     title=f"Network with iteration of removal")
    if save:
        file_path = output_dir / f"network_iteration_of_removal_results_{test_name}.png"
        plt.savefig(file_path)
    else:
        plt.show()

    ax = results_df_opt.plot(kind='line', x="iteration", y="flow_of_removed_edge",
                             color='blue', label="Bike flow", grid=True, title=f"Results for {test_name}")

    results_df_opt.plot(kind='line', x="iteration", y="modal_share_bike",
                        color='red', label="Modal share bike", secondary_y=True, ax=ax)

    if save:
        file_path = output_dir / f"graph_results_{test_name}.png"
        plt.savefig(file_path)
    else:
        plt.show()

    list_budget = list(range(1, 49))
    for budget in list_budget:
        plot_optimization_network(edge_df, edge_df_results,node_df, budget, save, output_dir_infra, output_dir_network, test_name)

def plot_optimization_different_budgets(list_test_name:list, list_budget:list, save = False):
    for test_name in list_test_name:
        edge_df, node_df = import_network("data/edges_small_grid_2.csv", "data/nodes_small_grid_2.csv")
        results_df_opt = pd.read_csv(f"output/optimization/rgo_results_df_opt_{test_name}.csv")

        edge_df = edge_df.merge(results_df_opt, how="inner", left_index=True, right_on="index_removed").set_index(
            edge_df.index)

        edge_df.drop(
            ["Unnamed: 0", "nbr_bike_lanes", "nbr_none_bike_lanes", "modal_share_car", "modal_share_bike",
             "index_removed",
             "flow_of_removed_edge"], axis=1, inplace=True)
        edge_df.rename(columns={'iteration': 'iteration_of_removal'}, inplace=True)
        fig, ax = plt.subplots(1, len(list_budget), figsize=(10*len(list_budget), 10))
        i = 0
        for budget in list_budget:
            max_budget = max(edge_df["iteration_of_removal"])
            iteration_corresponding_to_budget = max_budget - budget + 1

            mask = edge_df["iteration_of_removal"] >= iteration_corresponding_to_budget
            list_index_of_bike_infra = edge_df.index[mask].tolist()

            edge_df = change_type_bike_infra_with_index(edge_df, "bike_path", list_index_of_bike_infra)
            plot_network(edge_df, node_df, node_id_col='node',
                         node_label=True,
                         color_col_str='type_bike',
                         base_width=1,
                         legend=True,
                         title=f"Network for a budget of {budget}", ax=ax[i])
            i += 1
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.suptitle(f'Networks for {test_name}', fontsize=20, fontweight='bold')
        if save:
            plt.savefig(f"output/optimization/images/{test_name}/networks_for_different_budgets_{test_name}.png")
        else :
            plt.show()