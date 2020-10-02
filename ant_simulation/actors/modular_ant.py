import math
import random
from typing import Union
from ant_simulation.behaviours.direction_management import Direction
from ant_simulation.behaviours.wander_pheromone_behaviour import WanderPheromoneBehaviour
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
    HOLD_POSITION_CHANCE: float = 0.2
    PHEROMONES_PER_TICK: int = 10
    INITIAL_BIAS_HOLDNESS_WOBBLE: (float, float, float) = 0.1, 10, 0.3
    INTERACTION_RADIUS: int = 2

    # Indicates the largest ModularAnt id taken so far (-1 if no id has yet been taken).
    max_ant_id: int = -1

    # Interactions dictionary:
    interactions = {}


    @staticmethod
    def create(attributes: Attributes = None, kinds: [Kind] = []) -> Actor:
        return ModularAnt(attributes, kinds)


    @staticmethod
    def get_id() -> str:
        return ModularAnt.ID


    @staticmethod
    def can_interact(a1, a2) -> bool:
        """\
    :type a1: ModularAnt
    :type a2: ModularAnt
        """
        SIMILARITY_THRESHOLD: float = 1
        return -1 * SIMILARITY_THRESHOLD <= Direction.dif_mag(a1.get_facing(), a2.get_facing().reversed()) <= SIMILARITY_THRESHOLD


    @staticmethod
    def log_interaction(a1, a2):
        """\
    :type a1: ModularAnt
    :type a2: ModularAnt
        """
        id1: int = a1.get_ant_id()
        id2: int = a2.get_ant_id()
        entry: (int, int) = (min(id1, id2), max(id1, id2))
        if entry in ModularAnt.interactions:
            ModularAnt.interactions[entry] += 1
        else:
            ModularAnt.interactions[entry] = 1


    def get_attributes_string(self) -> str:
        return repr([("age", self.age), ("bias", self.bias), ("holdness", self.holdness),
                ("wobble", self.wobble), ("hold_position_chance", self.hold_position_chance)])


    def get_colour(self) -> Colour:
        return ModularAnt.COLOUR.get_alt_blue(int((2/math.pi) * Colour.MAX_VALUE * math.atan(
            self.age/ModularAnt.AGE_COLOURING_PERIOD)
        ))


    def move(self, frm: Location, to: Location):
        to.set_actor(self)
        frm.remove_actor()


    def tick(self, world: World, elapsed: float, location: Location, position: Position):
        self.age += elapsed

        if random.random() > self.hold_position_chance:
            self.current_wander_behaviour.do(world, elapsed, location, position, self)

        location.add_pheromones(ModularAnt.PHEROMONES_PER_TICK)

        # Measure interactions:
        for loc in world.get_adjacent_locations(position.x, position.y, ModularAnt.INTERACTION_RADIUS, False):
            if loc.get_actor() is None:
                continue
            if isinstance(loc.get_actor(), ModularAnt):
                other: ModularAnt = loc.get_actor()
                if ModularAnt.can_interact(self, other):
                    ModularAnt.log_interaction(self, other)


    def get_facing(self) -> Direction:
        return self.current_wander_behaviour.facing


    def get_ant_id(self) -> int:
        return self.ant_id


    def __init__(self, attributes: Union[Attributes, None], kinds: [Kind]):
        super().__init__(kinds)

        # AI attributes.
        self.bias, self.holdness, self.wobble = ModularAnt.INITIAL_BIAS_HOLDNESS_WOBBLE
        self.hold_position_chance: float = ModularAnt.HOLD_POSITION_CHANCE
        self.age: float = 0
        if attributes is not None:
            # Overwrite (potentially all) attributes with input values.
            attributes.set_for(self)

        # ID-related attributes, forcibly controlled by the ant.
        self.ant_id = (ModularAnt.max_ant_id + 1)
        ModularAnt.max_ant_id += 1

        # Create a behaviour for it.
        self.current_wander_behaviour: WanderPheromoneBehaviour = WanderPheromoneBehaviour(self.bias, self.holdness, self.wobble)
