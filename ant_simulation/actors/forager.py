from ant_simulation.actors.ant import Ant
from architecture.actor import Actor
from architecture.kinds import Kind
from architecture.rendering.colour import Colour


class Forager(Ant):
    ID: str = "Forager"
    COLOUR: Colour = Colour(255,128,0)

    @staticmethod
    def create(kinds: [Kind] = []) -> Actor:
        return Forager(kinds)

    @staticmethod
    def get_id() -> str:
        return Forager.ID

    @staticmethod
    def get_colour() -> Colour:
        return Forager.COLOUR

    def __init__(self, kinds: [Kind]):
        super().__init__(kinds)