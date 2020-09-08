from ant_simulation.actors.ant import Ant
from architecture.actor import Actor
from architecture.kinds import Kind
from architecture.rendering.colour import Colour


class Forager(Ant):

    @staticmethod
    def create(kinds: [Kind] = []) -> Actor:
        return Forager(kinds)

    @staticmethod
    def get_id() -> str:
        return("Forager")

    @staticmethod
    def get_colour() -> Colour:
        return Colour(255,165,0)

    def __init__(self, kinds: [Kind]):
        super().__init__(kinds)