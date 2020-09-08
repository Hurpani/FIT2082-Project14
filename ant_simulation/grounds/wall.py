from architecture.ground import Ground
from architecture.kinds import Kind
from architecture.position import Position
from architecture.rendering.colour import Colour


class Wall(Ground):

    IS_PASSABLE: bool = False
    ID: str = "Wall"
    COLOUR: Colour = Colour(0, 0, 0)

    @staticmethod
    def create(kinds: [Kind] = []) -> Ground:
        return Wall(kinds)


    @staticmethod
    def get_id() -> str:
        return(Wall.ID)


    def is_passable(self) -> bool:
        return Wall.IS_PASSABLE


    def get_kinds(self) -> [Kind]:
        return self.kinds


    def add_kind(self, kind: Kind):
        self.kinds.append(kind)


    @staticmethod
    def get_colour() -> Colour:
        return Wall.COLOUR


    def __init__(self, kinds: [Kind]):
        super().__init__(kinds)
