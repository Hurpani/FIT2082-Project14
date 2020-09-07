
from architecture.rendering.colour import Colour
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import colors

class Plotter:
    """\

    """

    def draw_world(world):
        """\
    Draws a World in its current state.
        """
        colours: [[Colour]] = world.get_printable()

        colour_list_of_list = []
        cmap = []
        colour_dict = {}
        for i in range(len(colours)):
            colour_list_of_list.append([])
            for j in range(len(colours[0])):
                if colours[i][j].get_rgba() not in colour_dict:
                    colour_dict[colours[i][j].get_rgba()] = len(colour_dict)
                    cmap.append(colours[i][j].get_rgba())
                colour_list_of_list[i].append(colour_dict[colours[i][j].get_rgba()])
        for line in colour_list_of_list:
            print(line)
        cmap = mpl.colors.ListedColormap(cmap)
        plt.figure(figsize=(len(colour_list_of_list[0]), len(colour_list_of_list)))
        plt.axis("off")
        plt.pcolor(colour_list_of_list[::-1], cmap=cmap)
        plt.show()


