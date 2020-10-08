from typing import Union

from ant_simulation.actors.modular_ant import ModularAnt
from ant_simulation.behaviours.queen_wander_pheromone_behaviour import QueenWanderPheromoneBehaviour
from architecture.actor import Actor
from architecture.attributes import Attributes
from architecture.kinds import Kind
from architecture.location import Location
from architecture.position import Position
from architecture.rendering.colour import Colour
from architecture.world import World


class ModularQueen(ModularAnt):
    QUEEN_LOGICAL_AGE: float = 25
    BROOD_PHEROMONES_PER_TICK: int = 20
    HOLD_POSITION_CHANCE: float = 0.7
    COLOUR: Colour = Colour(255, 32, 240)
    ID: str = "mqu"

    @staticmethod
    def create(attributes: Attributes = None, kinds: [Kind] = []) -> Actor:
        return ModularQueen(attributes, kinds)


    @staticmethod
    def get_id() -> str:
        return ModularQueen.ID


    def get_colour(self) -> Colour:
        return ModularQueen.COLOUR


    def get_attributes_string(self) -> str:
        return repr([("age", self.age), ("bias", self.bias), ("holdness", self.holdness),
                ("wobble", self.wobble), ("hold_position_chance", self.hold_position_chance),
                     ("brood_position", self.brood_position)])


    def tick(self, world: World, elapsed: float, location: Location, position: Position):
        if self.brood_position is None:
            self.brood_position = (position.x, position.y)
            self.current_wander_behaviour.set_brood_position(self.brood_position)
        # location.add_brood_pheromones(ModularQueen.BROOD_PHEROMONES_PER_TICK)
        for loc in world.get_adjacent_locations(position.x, position.y, 1, False):
            loc.add_brood_pheromones(ModularQueen.BROOD_PHEROMONES_PER_TICK)
        self.current_wander_behaviour.set_age(ModularQueen.QUEEN_LOGICAL_AGE)
        super().tick(world, elapsed, location, position)


    def __init__(self, attributes: Union[Attributes, None], kinds: [Kind]):
        if Kind.QUEEN not in kinds:
            kinds.append(Kind.QUEEN)
        super().__init__(attributes, kinds)
        self.brood_position: Union[Position, None] = None
        self.hold_position_chance: float = ModularQueen.HOLD_POSITION_CHANCE
        attributes.set_for(self)
        self.current_wander_behaviour = QueenWanderPheromoneBehaviour(self.bias, self.holdness, self.wobble)
        if self.brood_position is not None:
            self.current_wander_behaviour.set_brood_position(self.brood_position)
