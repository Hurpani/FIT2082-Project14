from architecture.ground import Ground
from architecture.kinds import Kind
from architecture.position import Position
from architecture.rendering.colour import Colour


class ForageGrounds(Ground):

    ID: str = "ForageGrounds"
    IS_PASSABLE: bool = True
    COLOUR: Colour = Colour(0, 255, 120)

    @staticmethod
    def create(kinds: [Kind] = []) -> Ground:
        return ForageGrounds(kinds)


    @staticmethod
    def get_id() -> str:
        return(ForageGrounds.ID)


    def is_passable(self) -> bool:
        return ForageGrounds.IS_PASSABLE


    def get_kinds(self) -> [Kind]:
        return self.kinds


    def add_kind(self, kind: Kind):
        self.kinds.append(kind)


    @staticmethod
    def get_colour() -> Colour:
        return ForageGrounds.COLOUR


    def __init__(self, kinds: [Kind]):
        super().__init__(kinds)