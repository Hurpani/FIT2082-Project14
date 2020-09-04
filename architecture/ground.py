from abc import ABC, abstractmethod

from architecture.kinds import Kind


class Ground(ABC):
    """\
A piece of ground participating in the simulation.
    """
    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def is_passable(self) -> bool:
        pass

    def get_kinds(self) -> [Kind]:
        return []

    def __init__(self):
        pass