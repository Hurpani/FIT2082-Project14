from abc import ABC, abstractmethod

from architecture.kinds import Kind


class Object(ABC):
    """\
An object that actors can interact with, which is participating
in the simulation.
    """
    @abstractmethod
    def get_id(self) -> str:
        pass

    def get_kinds(self) -> [Kind]:
        return []

    def __init__(self):
        pass