from abc import ABC, abstractmethod


class Writeable(ABC):
    """\
The Writeable abstract base class. Provides an interface for objects in the simulation
    which can be written to a file.
    """

    @abstractmethod
    def get_writeout_string(self, x: int, y: int) -> str:
        pass
