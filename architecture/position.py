

class Position:
    """\
The Position class. Manages a position in a world, for actors to quickly
    find adjacent locations, or change their own.
    """

    def __init__(self, x: int = 0, y: int = 0):
        self.x: int = x
        self.y: int = y

    def get_coordinates(self) -> (int, int):
        return self.x, self.y