from architecture.rendering.colour import Colour
from architecture.world import World


class Plotter:
    """\

    """

    def draw_world(self, world: World):
        """\
    Draws a World in its current state.
        """
        colours: [[Colour]] = world.get_printable()
