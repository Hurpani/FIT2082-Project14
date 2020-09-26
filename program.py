##############################
from __future__ import annotations
##############################
from ant_simulation.actors.modular_ant import ModularAnt
from architecture.generation import registry
from architecture.generation.world_builder import create_world
from architecture.rendering.plotter import Plotter
from architecture.world import World
import matplotlib.pyplot as plt
import networkx as nx

if __name__ == "__main__":
    registry.register()

    world: World = create_world("output.txt", "actors.txt", "empty.txt")
    for i in range(1):
        world.run(500)
        Plotter.draw_world(world)
    # TODO : Probably would want to export this data. Need a way of interpretting it and
    #  creating a network out of it.

    def exportDataToEdgeListFile():
        file = open("edge_list.txt","w")
        list_of_keys = sorted(list(ModularAnt.interactions))
        for item in list_of_keys:
            file.write(str(item[0])+" "+str(item[1])+" {'weight':" + str(ModularAnt.interactions[item]) +"}\n")
        file.close()
    exportDataToEdgeListFile()

    def create_and_view_networkx(minimum_show:int = 0):
        file = open("edge_list.txt", "rb")
        G = nx.read_edgelist(file)
        file.close()

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

        nx.draw_networkx(G, pos=pos, node_size=400, edge_color=weights, edge_cmap=plt.cm.hot, width=temp_list,alpha=0.8)
        plt.show()

    create_and_view_networkx(0)