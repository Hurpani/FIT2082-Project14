import matplotlib.pyplot as plt
import networkx as nx
import collections
import numpy as np

def remove_edge_weights_less_than(G, amount:int = 0):
    for edge in list(G.edges.data()):
        if int(edge[2]['weight']) < amount:
            G.remove_edge(*edge[:2])
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
    print(List)
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
    G = remove_edge_weights_less_than(G,5)
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

if __name__ == "__main__":
    #result = community_size_ratio_real_world()
    #file = open("output.csv","w")
    #for line in result:
    #    file.write(str(line[0]) + "," + str(line[1])+"," + str(line[2])+"\n")
    #file.close()
    file = open("C:/Users/Desktop/FIT2082/FIT2082-Project14/edge_list.txt", "rb")
    G = nx.read_edgelist(file)
    community_size_ratio(G)
    print("you need a connected graph")
    degree_distribution(G)
    eccentricity_l(G)
    file.close()

    G = nx.read_graphml("C:/Users/Desktop/FIT2082/6ant/Ant_Keller/weighted_network_col5_day" + "1" + ".graphml")
    community_size_ratio(G)
    degree_distribution(G)
    eccentricity_l(G)

