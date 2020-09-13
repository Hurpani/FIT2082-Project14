from enum import Enum


class Kind(Enum):
    """\
The Kind enum. Allows objects in a simulation to inform each other
    of special attributes, skills or traits they have.
    """
    DEFAULT: int = 0
    TRACKER: int = 1
