import math
import random

from typing import Union, TYPE_CHECKING, List, Dict
from ant_simulation.behaviours.direction_management import Direction
from ant_simulation.behaviours.wander_pheromone_behaviour import WanderPheromoneBehaviour
from ant_simulation.grounds.forage_grounds import ForageGrounds
from ant_simulation.grounds.nest import Nest
from ant_simulation.objects.food import Food
from architecture.actor import Actor
from architecture.attributes import Attributes
from architecture.kinds import Kind
from architecture.location import Location
from architecture.position import Position
from architecture.rendering.colour import Colour
from architecture.world import World

if TYPE_CHECKING:
    from architecture.object import Object


class ModularAnt(Actor):
    COLOUR: Colour = Colour(150, 127, 0)
    AGE_COLOURING_PERIOD: float = 200
    AGE_SCALE: float = 0.0001  # ages are being input in days, and each tick represents approx. 1s, so ~1/10000 scale.
    ID: str = "mant"
    HOLD_POSITION_CHANCE: float = 0.2
    PHEROMONES_PER_TICK: int = 4  # 8
    FORAGING_PHEROMONES_PER_TICK: int = 3
    FORAGING_AGE: int = 120  # 130
    FORAGING_PHEROMONE_OVERRIDE_CHANCE: float = 0.3
    INITIAL_BIAS_HOLDNESS_WOBBLE: (float, float, float) = 0.2, 40, 0.1
    INTERACTION_RADIUS: int = 2
    INTERACTIONS_FILE_NAME: str = "interactions.txt"
    INTERACTION_BREAK_DURATION: int = 6
    FOOD_DROP_CHANCE: float = 0.015
    ALT_PICKUP_CHANCE: float = 0.05

    # Indicates the largest ModularAnt id taken so far (-1 if no id has yet been taken).
    max_ant_id: int = -1

    # Interactions dictionary:
    interactions = {}

    # Age dictionary:
    initial_age_by_id: Dict[str, float] = {}

    @staticmethod
    def get_initial_age(id: str) -> float:
        return ModularAnt.initial_age_by_id[id] if id in ModularAnt.initial_age_by_id else 0.0

    @staticmethod
    def get_initial_ages() -> Dict[str, float]:
        return ModularAnt.initial_age_by_id

    @staticmethod
    def save_interactions():
        with open((World.WRITE_OUT_FILE_PATH / ModularAnt.INTERACTIONS_FILE_NAME), "w+") as file:
            file.write(str(ModularAnt.interactions))

    @staticmethod
    def get_interactions() -> List[str]:
        out_list: List[str] = []
        for uv, w in ModularAnt.interactions.items():
            out_list.append(f"{uv[0]} {uv[1]} {'{'}'weight':{ModularAnt.interactions[uv]}{'}'}")
        return out_list


    @staticmethod
    def get_interaction_count() -> int:
        return sum(ModularAnt.interactions.values())


    @staticmethod
    def load_interactions():
        with open((World.WRITE_OUT_FILE_PATH / ModularAnt.INTERACTIONS_FILE_NAME), "r") as file:
            ModularAnt.interactions = eval(file.read())

    @staticmethod
    def wipe_interactions():
        ModularAnt.interactions = {}

    @staticmethod
    def create(attributes: Attributes = None, kinds: [Kind] = []) -> Actor:
        return ModularAnt(attributes, kinds)

    @staticmethod
    def get_id() -> str:
        return ModularAnt.ID

    @staticmethod
    def can_interact(a1: "ModularAnt", a2: "ModularAnt") -> bool:
        SIMILARITY_THRESHOLD: float = 1
        return a1.sleep_interactions == a2.sleep_interactions == 0 and (a1.get_facing() - a2.get_facing().reversed()).\
            size_l1() <= SIMILARITY_THRESHOLD

    # @staticmethod
    # def can_interact(a1, a2) -> bool:
    #     """\
    # :type a1: ModularAnt
    # :type a2: ModularAnt
    #     """
    #     SIMILARITY_THRESHOLD: float = 1
    #     return (-1 * SIMILARITY_THRESHOLD <= Direction.dif_mag(a1.get_facing(),
    #                                                            a2.get_facing().reversed()) <= SIMILARITY_THRESHOLD)

    @staticmethod
    def log_interaction(a1, a2):
        """\
    :type a1: ModularAnt
    :type a2: ModularAnt
        """
        id1: int = a1.get_ant_id()
        id2: int = a2.get_ant_id()
        ModularAnt.log_interaction_ids(id1, id2)

    @staticmethod
    def log_interaction_ids(id1: int, id2: int):
        entry: (int, int) = (min(id1, id2), max(id1, id2))
        if random.random() > 0.5:
            if entry in ModularAnt.interactions:
                ModularAnt.interactions[entry] += 1
            else:
                ModularAnt.interactions[entry] = 1

    def get_attributes_string(self) -> str:
        return repr([("age", self.age), ("bias", self.bias), ("holdness", self.holdness),
                     ("wobble", self.wobble), ("hold_position_chance", self.hold_position_chance),
                     ("carrying_food", self.carrying_food), ("interacting_with_id", self.interacting_with_id),
                     ("interacting_ticks", self.interacting_ticks)])

    def get_colour(self) -> Colour:
        return ModularAnt.COLOUR.get_alt_blue(int((2 / math.pi) * Colour.MAX_VALUE * math.atan(
            self.age / ModularAnt.AGE_COLOURING_PERIOD)
                                                  ))

    def move(self, frm: Location, to: Location):
        to.set_actor(self)
        frm.remove_actor()

    def interact(self, other_id: int):
        self.interacting_ticks = 0
        self.interacting_with_id = -1
        self.sleep_interactions = ModularAnt.INTERACTION_BREAK_DURATION
        ModularAnt.log_interaction_ids(self.get_ant_id(), other_id)

    def tick(self, world: World, elapsed: float, location: Location, position: Position):
        self.age += elapsed * ModularAnt.AGE_SCALE
        self.sleep_interactions = max(0, self.sleep_interactions - elapsed)
        self.current_wander_behaviour.set_age(self.age)
        self.current_wander_behaviour.set_seeking_food(not self.carrying_food)

        if random.random() > self.hold_position_chance * (1 + self.interacting_ticks):
            # Shuffle the list of previous locations.
            if location != self.prev_location \
                    and self.prev_location != self.prev_prev_location \
                    and location != self.prev_prev_location:
                self.prev_prev_location = self.prev_location
                self.prev_location = location
            # end of ^.
            self.current_wander_behaviour.do(world, elapsed, location, position, self)

        if self.age < ModularAnt.FORAGING_AGE or random.random() < ModularAnt. \
                FORAGING_PHEROMONE_OVERRIDE_CHANCE:
            if self.prev_prev_location is not None:
                self.prev_prev_location.add_pheromones(ModularAnt.PHEROMONES_PER_TICK)
            # location.add_pheromones(ModularAnt.PHEROMONES_PER_TICK)
        else:
            if location.get_brood_pheromone_count() == 0 and location.get_pheromone_count() == 0:
                if self.prev_prev_location is not None:
                    self.prev_prev_location.add_foraging_pheromones(ModularAnt.FORAGING_PHEROMONES_PER_TICK)
                # location.add_foraging_pheromones(ModularAnt.FORAGING_PHEROMONES_PER_TICK)

        # If this ant is in the foraging area, it will pick up food readily.
        if not self.carrying_food:
            if location.get_ground().get_id() == ForageGrounds.get_id() or \
                    random.random() < ModularAnt.ALT_PICKUP_CHANCE:
                foods: [Object] = location.get_objects(Kind.FOOD)
                if len(foods) > 0:
                    self.carrying_food = True
                    location.remove_object(foods[-1])
        elif location.get_ground().get_id() == Nest.get_id():
            if random.random() < ModularAnt.FOOD_DROP_CHANCE or sum(map(lambda l: len(l.get_objects(Kind.FOOD)),
                                                                        world.get_adjacent_locations(position.x,
                                                                                                     position.y, 1,
                                                                                                     False))) > 0:
                location.add_object(Food())
                self.carrying_food = False

        # Measure interactions:
        others: [int] = []
        for loc in world.get_adjacent_locations(position.x, position.y, ModularAnt.INTERACTION_RADIUS, False):
            if loc.get_actor() is None:
                continue
            if isinstance(loc.get_actor(), ModularAnt):
                other: ModularAnt = loc.get_actor()
                if ModularAnt.can_interact(self, other):
                    others.append(other.get_ant_id())
        if self.interacting_with_id in others:
            self.interacting_ticks += 1
            if self.interacting_ticks > world.interacting_ticks_threshold:
                self.interact(self.interacting_with_id)
        elif len(others) > 0:
            self.interacting_with_id = others[0]
            self.interacting_ticks = 0

    def get_facing(self) -> Direction:
        return self.current_wander_behaviour.facing

    def get_ant_id(self) -> int:
        return self.ant_id

    def __init__(self, attributes: Union[Attributes, None], kinds: [Kind]):
        if Kind.ANT not in kinds:
            kinds.append(Kind.ANT)
        super().__init__(kinds)

        # AI attributes.
        self.bias, self.holdness, self.wobble = ModularAnt.INITIAL_BIAS_HOLDNESS_WOBBLE
        self.hold_position_chance: float = ModularAnt.HOLD_POSITION_CHANCE
        self.age: float = 0
        self.sleep_interactions: float = 0
        self.carrying_food: bool = False
        self.interacting_with_id: int = -1
        self.interacting_ticks: int = 0
        self.prev_location: Union[None, Location] = None
        self.prev_prev_location: Union[None, Location] = None
        if attributes is not None:
            # Overwrite (potentially all) attributes with input values.
            attributes.set_for(self)

        # ID-related attributes, forcibly controlled by the ant.
        self.ant_id = (ModularAnt.max_ant_id + 1)
        ModularAnt.max_ant_id += 1
        ModularAnt.initial_age_by_id[str(self.ant_id)] = self.age

        # Create a behaviour for it.
        self.current_wander_behaviour: WanderPheromoneBehaviour = WanderPheromoneBehaviour(self.bias, self.holdness,
                                                                                           self.wobble)
