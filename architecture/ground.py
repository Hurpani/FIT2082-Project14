from abc import abstractmethod
from architecture.kinds import Kind
from architecture.location import Location
from architecture.position import Position
from architecture.rendering.colour import Colour
from architecture.rendering.renderable import Renderable
from architecture.world import World


class Ground(Renderable):
    """\
A piece of ground participating in the simulation.
    """

    @staticmethod
    def create(kinds: [Kind] = []):
        pass


    @staticmethod
    def get_id() -> str:
        pass


    @abstractmethod
    def is_passable(self) -> bool:
        pass


    @abstractmethod
    def add_kind(self, kind: Kind):
        pass


    def get_kinds(self) -> [Kind]:
        return []


    def __init__(self, kinds: [Kind]):
        self.kinds = kinds


    def tick(self, world: World, elapsed: float, location: Location, position: Position):
        pass
