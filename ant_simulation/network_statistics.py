import matplotlib.pyplot as plt
import networkx as nx

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

if __name__ == "__main__":
    result = community_size_ratio_real_world()
    file = open("output.csv","w")
    for line in result:
        file.write(str(line[0]) + "," + str(line[1])+"," + str(line[2])+"\n")
    file.close()

