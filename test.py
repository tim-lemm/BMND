import matplotlib.pyplot as plt
import networkx as nx

from utils_plotting import *

city_name = "Sioux_Falls"
name_test = f"CAP_{city_name}_test_-0.001_-2_bi_11"
horodatage = "2026-08-25_11-07-44"
edge_df, node_df = import_network(f"data/{city_name}/edges_{city_name}.csv", f"data/{city_name}/nodes_{city_name}.csv", real_network=True)

def convert_edge_df_to_nx_graph(edge_df, node_df):
    G = nx.Graph()

    for _, row in node_df.iterrows():
        node_id = int(row['id'])
        attrs = row.to_dict()
        attrs['pos'] = (row['x'], row['y'])
        G.add_node(node_id, **attrs)

    for _, row in edge_df.iterrows():
        u = int(row['a_node'])
        v = int(row['b_node'])
        attrs = row.to_dict()
        del attrs['a_node']
        del attrs['b_node']

        G.add_edge(u, v, **attrs)

    return G

G = convert_edge_df_to_nx_graph(edge_df, node_df)
mst = nx.minimum_spanning_tree(G, weight='length')
pos = nx.get_node_attributes(G, 'pos')

plt.figure(figsize=(8, 10))

nx.draw_networkx(G, pos, alpha=0.5, edge_color='lightgray', style='dashed', width=1.5)
nx.draw_networkx(mst, pos, alpha=0.5, edge_color='green', width=2, label="Minimum spanning tree")

plt.title("Minimum spanning tree of the Sioux Falls network")
plt.show()

