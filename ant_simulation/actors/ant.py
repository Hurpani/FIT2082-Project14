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

    @staticmethod
    def create(kinds: [Kind] = []) -> Actor:
        return Ant(kinds)


    @staticmethod
    def get_id() -> str:
        return "ant"


    def get_kinds(self) -> [Kind]:
        return self.kinds


    def tick(self, world: World, elapsed: float, location: Location, position: Position):
        pass


    def add_kind(self, kind: Kind):
        self.kinds.append(kind)

    def get_colour(self) -> Colour:
        return Colour()


    def __init__(self, kinds: [Kind]):
        super().__init__(kinds)








