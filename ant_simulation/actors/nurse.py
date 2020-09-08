from ant_simulation.actors.ant import Ant
from architecture.actor import Actor
from architecture.kinds import Kind
from architecture.rendering.colour import Colour


class Nurse(Ant):
    ID: str = "Nurse"
    COLOUR: Colour = Colour(0, 0, 205)

    @staticmethod
    def create(kinds: [Kind] = []) -> Actor:
        return Nurse(kinds)

    @staticmethod
    def get_id() -> str:
        return Nurse.ID

    @staticmethod
    def get_colour() -> Colour:
        return Nurse.COLOUR

    def __init__(self, kinds: [Kind]):
        super().__init__(kinds)
