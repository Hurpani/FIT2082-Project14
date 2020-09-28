import matplotlib.pyplot as plt
import networkx as nx


def export_data_to_edge_list_file(dct: {}):
    file = open("edge_list.txt", "w")
    list_of_keys = sorted(list(dct))
    for item in list_of_keys:
        file.write(str(item[0]) + " " + str(item[1]) + " {'weight':" + str(dct[item]) + "}\n")
    file.close()

def create_and_view_networkx(input_file: str, minimum_show: int = 0):
    # all that is needed to create a networkx Graph
    file = open(input_file, "rb")
    G = nx.read_edgelist(file)
    file.close()

    # code for edge widths and colours
    for edge in list(G.edges.data()):
        if int(edge[2]['weight']) < minimum_show:
            G.remove_edge(*edge[:2])

    pos = nx.fruchterman_reingold_layout(G)
    for x in [x for x in G.nodes() if G.degree(x) == 0]:
        G.remove_node(x)
    temp_list = []
    edges, weights = zip(*nx.get_edge_attributes(G, 'weight').items())
    for i in range(len(weights)):
        temp_list.append(weights[i] / 5)

    # write pajek file
    nx.write_pajek(G, "test.net")

    # show network to user
    nx.draw_networkx(G, pos=pos, node_size=400, edge_color=weights, edge_cmap=plt.cm.hot, width=temp_list, alpha=0.8)
    plt.show()
