import matplotlib.pyplot as plt
import networkx as nx
import collections
import numpy as np
import random as random
import csv
def create_random_graph_based_off(G):
    #create a random graph with same number of nodes and edges
    F = nx.generators.random_graphs.gnm_random_graph(G.number_of_nodes(),G.number_of_edges())

    #work out total weight of edges in base graph
    total_weight = 0
    for edge in list(G.edges.data()):
        total_weight += int(edge[2]['weight'])
    #assign each edge with a weight of 1 and take that away from the total weight amount
    total_weight -= F.number_of_edges()
    for edge in list(F.edges.data()):
        edge[2]['weight'] = 1

    #generate a list of edges of a length total_weight with replacment from F.edges, then add a weight to each sample
    print(list(F.edges.data()))
    edge_list = random.choices(list(F.edges.data()),k=total_weight)
    for edge in edge_list:
        edge[2]['weight'] +=1

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

def community_size_ratio(G,display:bool = True):
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
    #print(List)
    if display == True:
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
    counter = []
    diameter_list = []

    for node in G:
        if nx.eccentricity(G, node) > len(diameter_list)-1:
            for i in range(len(diameter_list),nx.eccentricity(G, node)+1):
                if len(counter) == 0:
                    counter.append(0)
                else:
                    counter.append(i)
                diameter_list.append(0)
        diameter_list[nx.eccentricity(G,node)] += 1
    plt.bar(counter,diameter_list , width=0.80, color="b")
    plt.title("Eccentricity of Network")
    plt.xlabel("eccentricity of node")
    plt.ylabel("amount of nodes with that eccentricity")
    plt.show()

def clustering_l(G):
    counter = [0]
    clustering_list = [0]

    for node in G:
        counter.append(counter[-1] + 1)
        clustering_list.append((nx.clustering(G, node, "weight")))

    clustering_list.sort()

    plt.plot(counter,clustering_list , color="b")
    plt.title("Clustering of Network")
    plt.xlabel("node")
    plt.ylabel("clustering coefficient")
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

def indivualGraphs():
    # Random
    colony = 5
    day = 1
    G = nx.read_graphml(
        "C:/Users/Desktop/FIT2082/6ant/Ant_Keller/weighted_network_col" + str(colony) + "_day" + str(day) + ".graphml")
    F = create_random_graph_based_off(G)

    total_weight = 0
    for edge in list(F.edges.data()):
        total_weight += int(edge[2]['weight'])
    print(total_weight)

    Fc = F.subgraph(max(nx.connected_components(F))).copy()
    remove_edge_weights_less_than(Fc, 15)
    Fc = Fc.subgraph(max(nx.connected_components(Fc))).copy()
    showGraph(Fc)
    community_size_ratio(Fc)
    degree_distribution(Fc)
    eccentricity_l(Fc)
    clustering_l(Fc)

    # Simulation
    file = open("C:/Users/Desktop/FIT2082/FIT2082-Project14/edge_list.txt", "rb")
    G = nx.read_edgelist(file)
    file.close()

    total_weight = 0
    for edge in list(G.edges.data()):
        total_weight += int(edge[2]['weight'])
    print(total_weight)

    remove_edge_weights_less_than(G, 20)
    G = G.subgraph(max(nx.connected_components(G))).copy()
    showGraph(G)
    community_size_ratio(G)
    degree_distribution(G)
    eccentricity_l(G)
    clustering_l(G)

    # real world
    colony = 5
    day = 1
    G = nx.read_graphml(
        "C:/Users/Desktop/FIT2082/6ant/Ant_Keller/weighted_network_col" + str(colony) + "_day" + str(day) + ".graphml")

    total_weight = 0
    for edge in list(G.edges.data()):
        total_weight += int(edge[2]['weight'])
    print(total_weight)

    remove_edge_weights_less_than(G, 20)
    G = G.subgraph(max(nx.connected_components(G))).copy()
    showGraph(G)
    community_size_ratio(G)
    degree_distribution(G)
    eccentricity_l(G)
    clustering_l(G)

def lots_of_graphs():
    Simualation_community = [[], [], []]
    Simualation_degree, Simualation_clustering, Simualation_eccentricity = [], [], []
    list_of_file_names = ["C:/Users/Desktop/FIT2082/FIT2082-Project14/edge_list.txt"]
    for file in list_of_file_names:
        G = nx.read_edgelist(file)
        remove_edge_weights_less_than(G, 700)
        G = G.subgraph(max(nx.connected_components(G))).copy()
        communities = community_size_ratio(G, False)
        Simualation_community[0].append(communities[0])
        Simualation_community[1].append(communities[1])
        Simualation_community[2].append(communities[2])
        Simualation_degree.append(sum([d for n, d in G.degree()]) / len([d for n, d in G.degree()]))
        temp = []
        for node in G.nodes():
            temp.append(nx.eccentricity(G, node))
        Simualation_eccentricity.append(sum(temp) / len(temp))
        Simualation_clustering.append(nx.average_clustering(G, weight='weight'))
    file = open("simulation.csv", "w+")

    with file:
        write = csv.writer(file)
        write.writerows(Simualation_community)
        write.writerow(Simualation_degree)
        write.writerow(Simualation_eccentricity)
        write.writerow(Simualation_clustering)
    file.close()

    colony = 5
    Real_community = [[], [], []]
    Real_degree, Real_clustering, Real_eccentricity = [], [], []
    for day in range(1, 42):
        print("Real " + str(day))
        G = nx.read_graphml(
            "C:/Users/Desktop/FIT2082/6ant/Ant_Keller/weighted_network_col" + str(colony) + "_day" + str(
                day) + ".graphml")
        remove_edge_weights_less_than(G, 10)
        G = G.subgraph(max(nx.connected_components(G))).copy()
        communities = community_size_ratio(G, False)
        Real_community[0].append(communities[0])
        Real_community[1].append(communities[1])
        Real_community[2].append(communities[2])
        Real_degree.append(sum([d for n, d in G.degree()]) / len([d for n, d in G.degree()]))
        temp = []
        for node in G.nodes():
            temp.append(nx.eccentricity(G, node))
        Real_eccentricity.append(sum(temp) / len(temp))
        Real_clustering.append(nx.average_clustering(G, weight='weight'))
    file = open("real.csv", "w+")
    with file:
        write = csv.writer(file)
        write.writerows(Real_community)
        write.writerow(Real_degree)
        write.writerow(Real_eccentricity)
        write.writerow(Real_clustering)
    file.close()

    file = open("random.csv", "w")
    colony = 5
    Random_community = [[], [], []]
    Random_degree, Random_clustering, Random_eccentricity = [], [], []
    for day in range(1, 42):
        print("Random " + str(day))
        G = nx.read_graphml(
            "C:/Users/Desktop/FIT2082/6ant/Ant_Keller/weighted_network_col" + str(colony) + "_day" + str(
                day) + ".graphml")
        G = create_random_graph_based_off(G)
        remove_edge_weights_less_than(G, 10)
        G = G.subgraph(max(nx.connected_components(G))).copy()
        communities = community_size_ratio(G, False)
        Random_community[0].append(communities[0])
        Random_community[1].append(communities[1])
        Random_community[2].append(communities[2])
        Random_degree.append(sum([d for n, d in G.degree()]) / len([d for n, d in G.degree()]))
        temp = []
        for node in G.nodes():
            temp.append(nx.eccentricity(G, node))
        Random_eccentricity.append(sum(temp) / len(temp))
        Random_clustering.append(nx.average_clustering(G, weight='weight'))
    file = open("Random.csv", "w+")
    with file:
        write = csv.writer(file)
        write.writerows(Random_community)
        write.writerow(Random_degree)
        write.writerow(Random_eccentricity)
        write.writerow(Random_clustering)
    file.close()

if __name__ == "__main__":
    indivualGraphs()


