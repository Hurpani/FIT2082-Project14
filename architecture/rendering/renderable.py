from abc import ABC, abstractmethod
from architecture.rendering.colour import Colour


class Renderable(ABC):
    """\
The Renderable abstract class. Allows objects in the simulation to be
    drawn.
    """

    @abstractmethod
    def get_colour(self) -> Colour:
        pass