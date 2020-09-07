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

    def get_colour(self) -> Colour:
        return Colour()


    def __init__(self, pos: Position, kinds: [Kind]):
        self.kinds = kinds
        self.pos = pos
        self.is_free = False

class Nurse(Ant):

    def create(self, pos: Position = Position(), kinds: [Kind] = []) -> Actor:
        return Nurse(pos, kinds)

    @staticmethod
    def get_id() -> str:
        return "Nurse"


    def get_kinds(self) -> [Kind]:
        return self.kinds


    def tick(self, world: World, elapsed: float, location: Location):
        pass


    def add_kind(self, kind: Kind):
        self.kinds.append(kind)

    @staticmethod
    def get_colour() -> Colour:
        return Colour(0,0,205)


    def __init__(self, pos: Position, kinds: [Kind]):
        self.kinds = kinds
        self.pos = pos
        self.is_free = False

class Cleaner(Ant):

    def create(self, pos: Position = Position(), kinds: [Kind] = []) -> Actor:
        return Cleaner(pos, kinds)

    @staticmethod
    def get_id() -> str:
        return("Cleaner")


    def get_kinds(self) -> [Kind]:
        return self.kinds


    def tick(self, world: World, elapsed: float, location: Location):
        pass


    def add_kind(self, kind: Kind):
        self.kinds.append(kind)

    @staticmethod
    def get_colour() -> Colour:
        return Colour(50,205,0)


    def __init__(self, pos: Position, kinds: [Kind]):
        self.kinds = kinds
        self.pos = pos
        self.is_free = False

class Foarager(Ant):

    def create(self, pos: Position = Position(), kinds: [Kind] = []) -> Actor:
        return Foarager(pos, kinds)

    @staticmethod
    def get_id() -> str:
        return("Forager")


    def get_kinds(self) -> [Kind]:
        return self.kinds


    def tick(self, world: World, elapsed: float, location: Location):
        pass


    def add_kind(self, kind: Kind):
        self.kinds.append(kind)

    @staticmethod
    def get_colour() -> Colour:
        return Colour(255,165,0)

    def __init__(self, pos: Position, kinds: [Kind]):
        self.kinds = kinds
        self.pos = pos
        self.is_free = False

class Queen(Ant):

    def create(self, pos: Position = Position(), kinds: [Kind] = []) -> Actor:
        return Queen(pos, kinds)

    @staticmethod
    def get_id() -> str:
        return("Queen")


    def get_kinds(self) -> [Kind]:
        return self.kinds


    def tick(self, world: World, elapsed: float, location: Location):
        possible_free_locations = []
        for i in range(-1,2):
            for j in range(-1,2):
                if world.world[self.pos.get_coordinates[1]+i][self.pos.get_coordinates[0]+j].is_free():
                    possible_free_locations.append([self.pos.get_coordinates[1]+i,self.pos.get_coordinates[0]+j])
        print(possible_free_locations)


    def add_kind(self, kind: Kind):
        self.kinds.append(kind)

    @staticmethod
    def get_colour() -> Colour:
        return Colour(75,0,130)


    def __init__(self, pos: Position, kinds: [Kind]):
        self.kinds = kinds
        self.pos = pos
        self.is_free = False