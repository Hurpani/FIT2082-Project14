import matplotlib.pyplot as plt
import networkx as nx
import collections
import numpy as np
import random as random

def create_random_graph_based_off(G):
    #create a random graph with same number of nodes and edges
    F = nx.generators.random_graphs.gnm_random_graph(G.number_of_nodes(),G.number_of_edges())

    #work out total weight of edges in base graph
    total_weight = 0
    for edge in list(G.edges.data()):
        total_weight += int(edge[2]['weight'])

    #assign each edge with a weight of 1 and take that away from the total weight amount
    total_weight -= F.number_of_nodes()
    for edge in list(F.edges.data()):
        edge[2]['weight'] = 1

    #loop though edges 1% of the time adding a weight to that edge and de-incrementing total_weight
    #repeated until no more weights to add
    while total_weight > 0:
        for edge in list(F.edges.data()):
            if total_weight == 0:
                break

            if random.random() < 0.01:
                edge[2]['weight'] += 1
                total_weight -= 1

    return F



def remove_edge_weights_less_than(G, amount:int = 0):
    for edge in list(G.edges.data()):
        if int(edge[2]['weight']) < amount:
            G.remove_edge(*edge[:2])
    G.remove_nodes_from(list(nx.isolates(G)))
    return G

def community_size_networkx(input_file: str, amount_of_community:int = 3):
    file = open(input_file, "rb")
    G = nx.read_edgelist(file)
    file.close()
    for community in (nx.algorithms.community.asyn_fluid.asyn_fluidc(G,3)):
        print(len(community))

def community_size_ratio_real_world():
    MainList = []
    for i in range(1,42):
        G = nx.read_graphml("C:/Users/Desktop/FIT2082/6ant/Ant_Keller/weighted_network_col5_day" + str(i) + ".graphml")
        List = []
        for community in (nx.algorithms.community.asyn_fluid.asyn_fluidc(G,3)):
            List.append(len(community))
        List.sort()
        List.reverse()
        sumlist = sum(List)
        for i in range(len(List)):
            List[i] /= sumlist
        MainList.append(List)
    print(MainList)
    return MainList

def community_size_ratio(G):
    List = []
    for community in (nx.algorithms.community.asyn_fluid.asyn_fluidc(G,3)):
        List.append(len(community))
    List.sort()
    List.reverse()
    sumlist = sum(List)
    for i in range(len(List)):
        List[i] /= sumlist
        List[i] *= 100000
        List[i] = int(List[i])
        List[i] /= 1000
    print(List)
    plt.bar([0,1,2],List , width=0.80, color="b")
    plt.title("Community Size Comparision ")
    plt.ylabel("percentage of nodes in each community")
    plt.show()
    return List

def degree_distribution(G):
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    plt.bar(deg, cnt, width=0.80, color="b")
    plt.title("Degree Distribution of Network")
    plt.xlabel("size of degree")
    plt.ylabel("amount of nodes with that degree")
    plt.show()

def eccentricity_l(G):
    counter = [1]
    diameter_list = [0]

    for node in G:
        if nx.eccentricity(G, node) > len(diameter_list)-1:
            for i in range(len(diameter_list),nx.eccentricity(G, node)+1):
                counter.append(i)
                diameter_list.append(0)
        diameter_list[nx.eccentricity(G,node)] += 1
    plt.bar(counter,diameter_list , width=0.80, color="b")
    plt.title("Eccentricity of Network")
    plt.xlabel("eccentricity of node")
    plt.ylabel("amount of nodes with that eccentricity")
    plt.show()

def showGraph(G):
    pos = nx.fruchterman_reingold_layout(G)

    temp_list = []
    edges, weights = zip(*nx.get_edge_attributes(G, 'weight').items())
    for i in range(len(weights)):
        temp_list.append(weights[i]**0.05)  # **0.5

    # write pajek file
    nx.write_pajek(G, "test.net")

    # show network to user
    nx.draw_networkx(G, pos=pos, node_size=50, edge_color=weights, edge_cmap=plt.cm.hot, width=temp_list, alpha=0.8, with_labels=False)
    plt.show()
if __name__ == "__main__":

    #Random
    colony = 5
    day = 1
    G = nx.read_graphml("C:/Users/Desktop/FIT2082/6ant/Ant_Keller/weighted_network_col" + str(colony) + "_day" + str(day) + ".graphml")
    F = create_random_graph_based_off(G)
    remove_edge_weights_less_than(F, 15)
    Fc = F.subgraph(max(nx.connected_components(F))).copy()
    community_size_ratio(Fc)
    degree_distribution(Fc)
    eccentricity_l(Fc)
    showGraph(Fc)

    #Simulation
    file = open("C:/Users/Desktop/FIT2082/FIT2082-Project14/edge_list.txt", "rb")
    G = nx.read_edgelist(file)
    file.close()
    remove_edge_weights_less_than(G,800)
    community_size_ratio(G)
    degree_distribution(G)
    eccentricity_l(G)
    showGraph(G)

    #real world
    colony = 5
    day = 1
    G = nx.read_graphml("C:/Users/Desktop/FIT2082/6ant/Ant_Keller/weighted_network_col" + str(colony) + "_day" + str(day) + ".graphml")
    remove_edge_weights_less_than(G, 20)
    community_size_ratio(G)
    degree_distribution(G)
    eccentricity_l(G)
    showGraph(G)



