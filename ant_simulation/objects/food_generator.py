##############################
from __future__ import annotations

import random
from typing import TYPE_CHECKING
##############################
from ant_simulation.objects.food import Food
from architecture.object import Object
from architecture.kinds import Kind

if TYPE_CHECKING:
    from architecture.location import Location
    from architecture.position import Position
    from architecture.world import World


class FoodGenerator(Object):
    ID: str = "food_generator"
    RADIUS: int = 3
    CHANCE: float = 0.000025

    @staticmethod
    def get_id() -> str:
        return FoodGenerator.ID

    @staticmethod
    def create(kinds: [Kind] = []):
        return FoodGenerator(kinds)

    def tick(self, world: World, elapsed: float, location: Location, position: Position):
        if random.random() < FoodGenerator.CHANCE:
            for loc in world.get_adjacent_locations(position.x, position.y, FoodGenerator.RADIUS, False):
                if len(loc.get_objects(Kind.FOOD)) == 0:
                    loc.add_object(Food())

    def __init__(self, kinds: [Kind] = []):
        super().__init__(kinds)
