from typing import Callable, Dict
from architecture.actor import Actor
from architecture.exceptions.invalid_id import InvalidIdException
from architecture.ground import Ground
from architecture.position import Position

"""\
The Factory functions. Manages the generation of Actors and Grounds after their
registration.
"""

_actor_constructors: Dict[str, Callable[[Position], Actor]] = {}
_ground_constructors: Dict[str, Callable[[Position], Ground]] = {}


def register_actor(id: str, constructor: Callable[[Position], Actor]):
    """\
Registers an Actor's constructor against an id for generation.
    """
    _register(id, constructor, _actor_constructors)


def register_ground(id: str, constructor: Callable[[Position], Actor]):
    """\
Registers a Ground's constructor against an id for generation.
    """
    _register(id, constructor, _ground_constructors)


def make_actor(id: str, pos: Position = Position()) -> Actor:
    return _make(id, pos, _actor_constructors)


def make_ground(id: str, pos: Position = Position()) -> Ground:
    return _make(id, pos, _ground_constructors)


def _make(id: str, pos: Position, registry: Dict):
    if id in registry:
        return registry.get(id)(pos)
    else:
        raise InvalidIdException()


def _register(id: str, constructor: Callable, registry: Dict):
    if id not in registry:
        registry[id] = constructor
    else:
        raise InvalidIdException()
