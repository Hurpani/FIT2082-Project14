from typing import Callable, Dict, List
from architecture.actor import Actor
from architecture.ground import Ground
from architecture.position import Position
from architecture.exceptions.invalid_id import InvalidIdException
from architecture.kinds import Kind

"""\
The Factory functions. Manages the generation of Actors and Grounds after their
registration.
"""

_actor_constructors: Dict[str, Callable[[Position, List[Kind]], Actor]] = {}
_ground_constructors: Dict[str, Callable[[Position, List[Kind]], Ground]] = {}
_ground_colour_indices: Dict[str, int] = {}


def register_actor(id: str, constructor: Callable[[Position], Actor]):
    """\
Registers an Actor's constructor against an id for generation.
    """
    _register(id, constructor, _actor_constructors)


def register_ground(id: str, colour_index: int, constructor: Callable[[Position], Actor]):
    """\
Registers a Ground's constructor against an id for generation.
    """
    _register(id, constructor, _ground_constructors)
    _ground_colour_indices[id] = colour_index


def make_actor(id: str, *args) -> Actor:
    """\
Creates a new instance of the Actor class based on the provided string
    identifier.
    """
    return _make(id, _actor_constructors, *args)


def make_ground(id: str, *args) -> Ground:
    """\
Creates a new instance of the Ground class based on the provided string
    identifier.
    """
    return _make(id, _ground_constructors, *args)


def get_ground_colour_index(id: str) -> int:
    """\
Returns a numeric value for this ground, indicating the index into a list of colours
    used by MatPlotLib for rendering. It is okay for grounds to all return the same
    index if you want - this just means they'll render the same as each other.
    """
    if id in _ground_colour_indices:
        return _ground_colour_indices.get(id)
    else:
        raise InvalidIdException()


def _make(id: str, registry: Dict, *args):
    if id in registry:
        return registry.get(id)(*args)
    else:
        raise InvalidIdException()


def _register(id: str, constructor: Callable, registry: Dict):
    if id not in registry:
        registry[id] = constructor
    else:
        raise InvalidIdException()
