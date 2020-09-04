from architecture.location import Location


class World:
    """\
The Map class. Manages a piece of terrain for the simulation.
    """

    def __init__(self, scale: float):
        """\
    Constructor for the world class. Accepts a scale as an argument, which informs locations of
        their width and height.
        """
        self.scale: float = scale
        self.world: [[Location]] = []

    def get_scale(self) -> float:
        return self.scale

