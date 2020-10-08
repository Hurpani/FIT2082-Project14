# from random import random

from architecture.kinds import Kind
from architecture.location import Location
from architecture.object import Object
from architecture.position import Position
from architecture.world import World


class Brood(Object):
    ID: str = "brood"
    PHEROMONE_RADIUS: int = 3
    PHEROMONE_CHANCE: float = 0.4
    PHEROMONE_AMOUNT: int = 5

    @staticmethod
    def get_id() -> str:
        return Brood.ID


    @staticmethod
    def create(kinds: [Kind] = []):
        return Brood(kinds)


    def tick(self, world: World, elapsed: float, location: Location, position: Position):
        pass
        # for loc in world.get_adjacent_locations(position.x, position.y, Brood.PHEROMONE_RADIUS, False):
        #     if loc.get_actor() is not None:
        #         if Kind.ANT in loc.get_actor().get_kinds():
        #             if random() < Brood.PHEROMONE_CHANCE:
        #                 loc.add_brood_pheromones(Brood.PHEROMONE_AMOUNT)


    def __init__(self, kinds: [Kind] = []):
        super().__init__(kinds)
        self.kinds.append(Kind.BROOD)


