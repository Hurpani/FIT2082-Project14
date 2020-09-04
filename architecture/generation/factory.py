from collections import Callable
from architecture.actor import Actor
from architecture.exceptions.invalid_id import InvalidIdException
from architecture.ground import Ground
from architecture.position import Position

"""\
The Factory functions. Manages the generation of Actors and Grounds after their
registration.
"""

_actor_constructors: dict[str, Callable([], Actor)] = {}
_ground_constructors: dict[str, Callable([], Ground)] = {}


def register_actor(id: str, constructor: Callable([Position], Actor)):
    """\
Registers an Actor's constructor against an id for generation.
    """
    _register(id, constructor, _actor_constructors)


def register_ground(id: str, constructor: Callable([Position], Actor)):
    """\
Registers a Ground's constructor against an id for generation.
    """
    _register(id, constructor, _ground_constructors)


def make_actor(id: str, pos: Position) -> Actor:
    return _make(id, pos, _actor_constructors)


def make_ground(id: str, pos: Position) -> Ground:
    return _make(id, pos, _ground_constructors)


def _make(id: str, pos: Position, registry: dict):
    if id in registry:
        return registry[id](pos)
    else:
        raise InvalidIdException()


def _register(id: str, constructor: Callable, registry: dict):
    if id not in registry:
        registry[id] = constructor
    else:
        raise InvalidIdException()
