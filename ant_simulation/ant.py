from architecture.actor import Actor
from architecture.kinds import Kind
from architecture.location import Location
from architecture.position import Position
from architecture.rendering.colour import Colour
from architecture.world import World


class Ant(Actor):
    """\
A temporary test class.
    """
    def create(self, pos: Position = Position(), kinds: [Kind] = []) -> Actor:
        return Ant(pos, kinds)


    @staticmethod
    def get_id() -> str:
        return "ant"


    def get_kinds(self) -> [Kind]:
        return self.kinds


    def tick(self, world: World, elapsed: float, location: Location):
        pass


    def add_kind(self, kind: Kind):
        self.kinds.append(kind)

    @staticmethod
    def get_colour() -> Colour:
        return Colour(255,0,0)


    def __init__(self, pos: Position, kinds: [Kind]):
        self.kinds = kinds
        self.pos = pos


