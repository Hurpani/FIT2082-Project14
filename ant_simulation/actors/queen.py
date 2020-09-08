from ant_simulation.actors.ant import Ant
from architecture.actor import Actor
from architecture.kinds import Kind
from architecture.rendering.colour import Colour

class Queen(Ant):
    ID: str = "Queen"
    COLOUR: Colour = Colour(75, 0, 130)

    @staticmethod
    def create(kinds: [Kind] = []) -> Actor:
        return Queen(kinds)

    @staticmethod
    def get_id() -> str:
        return Queen.ID

    @staticmethod
    def get_colour() -> Colour:
        return Queen.COLOUR

    def __init__(self, kinds: [Kind]):
        super().__init__(kinds)