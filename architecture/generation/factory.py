from typing import Callable, Dict, List
from architecture.actor import Actor
from architecture.ground import Ground
from architecture.object import Object
from architecture.exceptions.invalid_id import InvalidIdException
from architecture.kinds import Kind

"""\
The Factory functions. Manages the generation of Actors and Grounds after their
registration.
"""

_actor_constructors: Dict[str, Callable[[List[Kind]], Actor]] = {}
_ground_constructors: Dict[str, Callable[[List[Kind]], Ground]] = {}
_object_constructors: Dict[str, Callable[[List[Kind]], Object]] = {}


def register_actor(id: str, constructor: Callable[[List[Kind]], Actor]):
    """\
Registers an Actor's constructor against an id for generation.
    """
    _register(id, constructor, _actor_constructors)


def register_ground(id: str, constructor: Callable[[List[Kind]], Ground]):
    """\
Registers a Ground's constructor against an id for generation.
    """
    _register(id, constructor, _ground_constructors)


def register_object(id: str, constructor: Callable[[List[Kind]], Object]):
    _register(id, constructor, _object_constructors)


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


def make_object(id: str, *args) -> Object:
    """\
Creates a new instance of the Object class based on the provided string
    identifier.
    """
    return _make(id, _actor_constructors, *args)


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
