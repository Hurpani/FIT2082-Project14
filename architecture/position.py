

class Position:
    """\
The Position class. Manages a position in a world, for actors to quickly
    find adjacent locations, or change their own.
    """

    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def get_coordinates(self) -> (int, int):
        return self.x, self.y