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
    def create(self, pos: Position = Position(), kinds: [Kind] = []):
        pass

    @staticmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def is_passable(self) -> bool:
        pass

    @abstractmethod
    def add_kind(self, kind: Kind):
        pass

    def get_kinds(self) -> [Kind]:
        return []

    def __init__(self, pos: Position, kinds: [Kind]):
        self.kinds = kinds
        self.pos = pos

    def tick(self, world: World, elapsed: float, location: Location):
        pass

class Tunnel(Ground):

    def create(self, pos: Position = Position(), kinds: [Kind] = []) -> Ground:
        return Tunnel(pos, kinds)


    @staticmethod
    def get_id() -> str:
        return "Tunnel"

    def is_passable(self) -> bool:
        return True

    def get_kinds(self) -> [Kind]:
        return self.kinds

    def add_kind(self, kind: Kind):
        self.kinds.append(kind)

    @staticmethod
    def get_colour() -> Colour:
        return Colour(255,255,255)

    def __init__(self, pos: Position, kinds: [Kind]):
        self.kinds = kinds
        self.pos = pos
        self.is_free = True

class Nest(Ground):

    def create(self, pos: Position = Position(), kinds: [Kind] = []) -> Ground:
        return Nest(pos, kinds)


    @staticmethod
    def get_id() -> str:
        return("Nest")

    def is_passable(self) -> bool:
        return True

    def get_kinds(self) -> [Kind]:
        return self.kinds

    def add_kind(self, kind: Kind):
        self.kinds.append(kind)

    @staticmethod
    def get_colour() -> Colour:
        return Colour(255, 255, 255)

    def __init__(self, pos: Position, kinds: [Kind]):
        self.kinds = kinds
        self.pos = pos
        self.is_free = True

class ForageGrounds(Ground):

    def create(self, pos: Position = Position(), kinds: [Kind] = []) -> Ground:
        return ForageGrounds(pos,kinds)

    @staticmethod
    def get_id() -> str:
        return("ForageGrounds")

    def is_passable(self) -> bool:
        return True

    def get_kinds(self) -> [Kind]:
        return self.kinds

    def add_kind(self, kind: Kind):
        self.kinds.append(kind)

    @staticmethod
    def get_colour() -> Colour:
        return Colour(255, 255, 255)

    def __init__(self, pos: Position, kinds: [Kind]):
        self.kinds = kinds
        self.pos = pos
        self.is_free = True

class Wall(Ground):
    def create(self, pos: Position = Position(), kinds: [Kind] = []) -> Ground:
        return Wall(pos, kinds)

    @staticmethod
    def get_id() -> str:
        return("Wall")

    def is_passable(self) -> bool:
        return False

    def get_kinds(self) -> [Kind]:
        return self.kinds

    def add_kind(self, kind: Kind):
        self.kinds.append(kind)

    @staticmethod
    def get_colour() -> Colour:
        return Colour(0,0,0)

    def __init__(self, pos: Position, kinds: [Kind]):
        self.kinds = kinds
        self.pos = pos
        self.is_free = False

