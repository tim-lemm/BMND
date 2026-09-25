from utils_plotting import *
from utils_network_processing import *
import networkx as nx


def build_networkx_graph(df_edges, df_nodes, source_col='a_node', target_col='b_node', node_id_col='node_id', create_using=nx.DiGraph()):
    """
    Convertit des DataFrames Pandas en un graphe NetworkX.

    Arguments:
    - df_edges : DataFrame contenant les arêtes (doit inclure source_col, target_col, et autres features).
    - df_nodes : DataFrame contenant les nœuds (doit inclure node_id_col, 'x', et 'y').
    - source_col : Nom de la colonne du nœud source dans df_edges.
    - target_col : Nom de la colonne du nœud cible dans df_edges.
    - node_id_col : Nom de la colonne de l'identifiant du nœud dans df_nodes.

    Retourne:
    - G : Un objet networkx.Graph (non orienté par défaut).
    """
    G = nx.from_pandas_edgelist(
        df_edges,
        source=source_col,
        target=target_col,
        edge_attr=True,
        create_using=create_using
    )
    node_attributes = df_nodes.set_index(node_id_col).to_dict('index')
    nx.set_node_attributes(G, node_attributes)

    return G

def graph_to_dataframes(G, source_col='a_node', target_col='b_node', node_id_col='id'):
    """
    Reconvertit un graphe NetworkX en deux DataFrames (arêtes et nœuds).

    Arguments :
    - G : L'objet networkx.Graph ou networkx.DiGraph.
    - source_col : Nom de la colonne source pour df_edges.
    - target_col : Nom de la colonne cible pour df_edges.
    - node_id_col : Nom de la colonne de l'identifiant du nœud pour df_nodes.

    Retourne :
    - df_edges : DataFrame contenant (source_col, target_col, id, + features).
    - df_nodes : DataFrame contenant (node_id_col, x, y, + attributs).
    """
    df_edges = nx.to_pandas_edgelist(G, source=source_col, target=target_col)
    nodes_data = [{node_id_col: node, **data} for node, data in G.nodes(data=True)]
    df_nodes = pd.DataFrame(nodes_data)

    return df_edges, df_nodes

def add_node_centralities(G, weight=None):
    """
    Calcule la degree, closeness et betweenness centrality des nœuds
    et les ajoute comme attributs au graphe G.

    Arguments :
    - G : Un objet networkx.Graph ou networkx.DiGraph.

    Retourne :
    - G : Le graphe enrichi des attributs de centralité.
    """
    # 1. Calcul des métriques de centralité
    degree_dict = nx.degree_centrality(G)
    closeness_dict = nx.closeness_centrality(G)
    betweenness_dict = nx.edge_betweenness_centrality(G, weight=weight)

    # 2. Ajout des métriques aux nœuds
    nx.set_node_attributes(G, degree_dict, 'degree_centrality')
    nx.set_node_attributes(G, closeness_dict, 'closeness_centrality')
    nx.set_edge_attributes(G, betweenness_dict, 'betweenness_centrality')

    return G

def add_edge_mean_from_nodes(G, node_attr, edge_attr_name=None, default_val=0.0):
    """
    Calcule la moyenne d'un attribut de nœud pour les deux extrémités de chaque arête
    et l'ajoute comme attribut d'arête.

    Arguments :
    - G : Le graphe NetworkX (Graph ou DiGraph).
    - node_attr : Nom de l'attribut de nœud à moyenner (ex: 'degree_centrality', 'x').
    - edge_attr_name : Nom de l'attribut d'arête généré (par défaut 'mean_<node_attr>').
    - default_val : Valeur de remplacement si un nœud n'a pas l'attribut.

    Retourne :
    - G : Le graphe enrichi du nouvel attribut d'arête.
    """
    if edge_attr_name is None:
        edge_attr_name = f"mean_{node_attr}"

    edge_values = {}
    for u, v in G.edges():
        val_u = G.nodes[u].get(node_attr, default_val)
        val_v = G.nodes[v].get(node_attr, default_val)
        edge_values[(u, v)] = (val_u + val_v) / 2.0

    nx.set_edge_attributes(G, edge_values, edge_attr_name)
    return G

list_test_name = ["grid","grid_2","H","clock","city",'city_2','tunnel']
# list_test_name = ["grid"]
for test_name in list_test_name:
    print(f"Testing {test_name}")
    edge_df, node_df = import_network(f"data/edges_{test_name}.csv", f"data/nodes_{test_name}.csv")
    edge_df = calculate_length_bi_3(edge_df)
    # convertion des graph en nx.Graph
    G = build_networkx_graph(edge_df, node_df, source_col='a_node', target_col='b_node', node_id_col='id')
    # calculs des métrics (mettre les valeurs dans les attributs)
    G = add_node_centralities(G, weight='length_bi')

    G = add_edge_mean_from_nodes(G, node_attr="degree_centrality")
    G = add_edge_mean_from_nodes(G, node_attr="closeness_centrality")
    # reconvertion en dfs
    edge_df, node_df = graph_to_dataframes(G)

    # plots
    fig, ax = plt.subplots(1,3, figsize=(30,10))
    plot_network(edge_df, node_df, node_id_col='id', base_width=1, node_label=True, title=f"Network with mean degree centrality",
                 ax=ax[0], color_col_num="mean_degree_centrality")
    plot_network(edge_df, node_df, node_id_col='id', base_width=1, node_label=True, title=f"Network with mean closeness centrality",
                 ax=ax[1], color_col_num="mean_closeness_centrality")
    plot_network(edge_df, node_df, node_id_col='id', base_width=1, node_label=True, title=f"Network with edge betweenness centrality",
                 ax=ax[2], color_col_num="betweenness_centrality")
    plt.show()

edge_df, node_df = import_network("data/Sioux_Falls/edges_Sioux_Falls.csv", "data/Sioux_Falls/nodes_Sioux_Falls.csv")
edge_df = calculate_length_bi_3(edge_df)
# convertion des graph en nx.Graph
G = build_networkx_graph(edge_df, node_df, source_col='a_node', target_col='b_node', node_id_col='id')
# calculs des métrics (mettre les valeurs dans les attributs)
G = add_node_centralities(G, weight='length_bi')

G = add_edge_mean_from_nodes(G, node_attr="degree_centrality")
G = add_edge_mean_from_nodes(G, node_attr="closeness_centrality")
# reconvertion en dfs
edge_df, node_df = graph_to_dataframes(G)

# plots
fig, ax = plt.subplots(1,3, figsize=(30,10))
plot_network(edge_df, node_df, node_id_col='id', base_width=1, node_label=True, title=f"Network with mean degree centrality",
                 ax=ax[0], color_col_num="mean_degree_centrality")
plot_network(edge_df, node_df, node_id_col='id', base_width=1, node_label=True, title=f"Network with mean closeness centrality",
                 ax=ax[1], color_col_num="mean_closeness_centrality")
plot_network(edge_df, node_df, node_id_col='id', base_width=1, node_label=True, title=f"Network with edge betweenness centrality",
                 ax=ax[2], color_col_num="betweenness_centrality")
plt.show()