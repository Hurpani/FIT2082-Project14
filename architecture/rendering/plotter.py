##############################
from __future__ import annotations
from typing import TYPE_CHECKING
##############################
if TYPE_CHECKING:
    from architecture.world import World

from architecture.rendering.colour import Colour
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import colors


class Plotter:
    """\
The Plotter class. Responsible for parsing a list of lists of colours, and drawing them
    in a grid to the screen.
    """

    def draw_world(world: World):

        """\
    Draws a World in its current state.
        """
        colours: [[Colour]] = world.get_printable()

        colour_list_of_list = []
        cmap = []
        colour_dict = {}
        for i in range(len(colours[0])):
            colour_list_of_list.append([])
            for j in range(len(colours)):
                if colours[j][i].get_rgba() not in colour_dict:
                    colour_dict[colours[j][i].get_rgba()] = len(colour_dict)
                    cmap.append(colours[j][i].get_rgba())
                colour_list_of_list[i].append(colour_dict[colours[j][i].get_rgba()])
        cmap = mpl.colors.ListedColormap(cmap)
        plt.figure(figsize=(len(colour_list_of_list[0]), len(colour_list_of_list)))
        plt.axis("off")
        plt.pcolor(colour_list_of_list[::-1], cmap=cmap)
        plt.show()


