from ant_simulation.actors.ant import Ant
from architecture.actor import Actor
from architecture.kinds import Kind
from architecture.rendering.colour import Colour

class Nurse(Ant):

    @staticmethod
    def create(kinds: [Kind] = []) -> Actor:
        return Nurse(kinds)

    @staticmethod
    def get_id() -> str:
        return "Nurse"

    @staticmethod
    def get_colour() -> Colour:
        return Colour(0,0,205)

    def __init__(self, kinds: [Kind]):
        super().__init__(kinds)