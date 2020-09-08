from architecture.ground import Ground
from architecture.kinds import Kind
from architecture.position import Position
from architecture.rendering.colour import Colour


class Nest(Ground):

    ID: str = "Nest"
    IS_PASSABLE: bool = True
    COLOUR: Colour = Colour(0, 255, 120)

    @staticmethod
    def create(kinds: [Kind] = []) -> Ground:
        return Nest(kinds)


    @staticmethod
    def get_id() -> str:
        return(Nest.ID)


    def is_passable(self) -> bool:
        return Nest.IS_PASSABLE


    def get_kinds(self) -> [Kind]:
        return self.kinds


    def add_kind(self, kind: Kind):
        self.kinds.append(kind)


    @staticmethod
    def get_colour() -> Colour:
        return Nest.COLOUR


    def __init__(self, kinds: [Kind]):
        super().__init__(kinds)