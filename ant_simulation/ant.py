from architecture.actor import Actor
from architecture.position import Position
from architecture.world import World


class Ant(Actor):
    """\
A temporary test class.
    """

    @staticmethod
    def create(pos: Position = Position()) -> Actor:
        return Ant(pos)

    @staticmethod
    def get_id() -> str:
        return "ant"

    def tick(self, elapsed: float, world: World):
        pass

    def __init__(self, pos: Position):
        pass


