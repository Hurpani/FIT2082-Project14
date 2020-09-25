import math
from typing import Union
from ant_simulation.behaviours.behaviour import Behaviour
from ant_simulation.behaviours.wander_pheromone_behaviour import WanderPheromoneBehaviour
from ant_simulation.objects.test_objects import TestObject
from architecture.actor import Actor
from architecture.attributes import Attributes
from architecture.kinds import Kind
from architecture.location import Location
from architecture.position import Position
from architecture.rendering.colour import Colour
from architecture.world import World


class ModularAnt(Actor):
    COLOUR: Colour = Colour(240, 127, 0)
    AGE_COLOURING_PERIOD: float = 200
    ID: str = "mant"
    PHEROMONES_PER_TICK: int = 1
    INITIAL_BIAS_HOLDNESS_WOBBLE: (float, float, float) = 0.025, 0.2, 0.3

    # Static field. Indicates the largest ModularAnt id taken so far (-1 if
    # no id has yet been taken).
    max_ant_id: int = -1

    @staticmethod
    def create(attributes: Attributes = None, kinds: [Kind] = []) -> Actor:
        return ModularAnt(attributes, kinds)

    @staticmethod
    def get_id() -> str:
        return ModularAnt.ID

    def get_colour(self) -> Colour:
        return ModularAnt.COLOUR.get_alt_blue(int((2/math.pi) * Colour.MAX_VALUE * math.atan(
            self.age/ModularAnt.AGE_COLOURING_PERIOD)
        ))

    def move(self, frm: Location, to: Location):
        to.set_actor(self)
        frm.remove_actor()

    def tick(self, world: World, elapsed: float, location: Location, position: Position):
        self.age += elapsed
        self.current_behaviour.do(world, elapsed, location, position, self)
        location.add_pheromones(ModularAnt.PHEROMONES_PER_TICK)
        location.add_object(TestObject())

    def __init__(self, attributes: Union[Attributes, None], kinds: [Kind]):
        super().__init__(kinds)
        self.ant_id = (ModularAnt.max_ant_id + 1)
        ModularAnt.max_ant_id += 1

        self.bias, self.holdness, self.wobble = ModularAnt.INITIAL_BIAS_HOLDNESS_WOBBLE
        self.age: float = 0
        if attributes is not None:
            attributes.set_for(self)

        self.current_behaviour: Behaviour = WanderPheromoneBehaviour(self.bias, self.holdness, self.wobble)
