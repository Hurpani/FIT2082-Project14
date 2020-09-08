from architecture.ground import Ground
from architecture.kinds import Kind
from architecture.position import Position
from architecture.rendering.colour import Colour


class Tunnel(Ground):

    ID: str = "Tunnel"
    IS_PASSABLE: bool = True
    COLOUR: Colour = Colour(255, 255, 255)

    @staticmethod
    def create(kinds: [Kind] = []) -> Ground:
        return Tunnel(kinds)


    @staticmethod
    def get_id() -> str:
        return Tunnel.ID


    def is_passable(self) -> bool:
        return Tunnel.IS_PASSABLE


    def get_kinds(self) -> [Kind]:
        return self.kinds


    def add_kind(self, kind: Kind):
        self.kinds.append(kind)


    @staticmethod
    def get_colour() -> Colour:
        return Tunnel.COLOUR


    def __init__(self, kinds: [Kind]):
        super().__init__(kinds)
