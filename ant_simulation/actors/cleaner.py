from ant_simulation.actors.ant import Ant
from architecture.actor import Actor
from architecture.kinds import Kind
from architecture.rendering.colour import Colour


class Cleaner(Ant):
    ID: str = "Cleaner"
    COLOUR: Colour = Colour(0, 100, 0)

    @staticmethod
    def create(kinds: [Kind] = []) -> Actor:
        return Cleaner(kinds)

    @staticmethod
    def get_id() -> str:
        return Cleaner.ID

    @staticmethod
    def get_colour() -> Colour:
        return Cleaner.COLOUR

    def __init__(self, kinds: [Kind]):
        super().__init__(kinds)
