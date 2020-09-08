from architecture.actor import Actor
from architecture.kinds import Kind
from architecture.location import Location
from architecture.position import Position
from architecture.rendering.colour import Colour
from architecture.world import World
import random

class Ant(Actor):
    """\
A temporary test class.
    """

    @staticmethod
    def create(kinds: [Kind] = []) -> Actor:
        return Ant(kinds)


    @staticmethod
    def get_id() -> str:
        return "ant"


    def get_kinds(self) -> [Kind]:
        return self.kinds


    def tick(self, world: World, elapsed: float, location: Location, pos: Position):
        possible_free_locations = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 and j != 0:
                    try:
                        if world.get_location(pos.get_coordinates()[0] + i, pos.get_coordinates()[1] + j).is_free():
                            possible_free_locations.append([pos.get_coordinates()[0] + i, pos.get_coordinates()[1] + j])
                    except:
                        pass
        if len(possible_free_locations) > 0:
            random_avalible_space = random.choice(possible_free_locations)
            world.get_location(pos.get_coordinates()[0], pos.get_coordinates()[1]).remove_actor()
            world.get_location(random_avalible_space[0], random_avalible_space[1]).set_actor(self)


    def add_kind(self, kind: Kind):
        self.kinds.append(kind)

    def get_colour(self) -> Colour:
        return Colour()


    def __init__(self, kinds: [Kind]):
        super().__init__(kinds)








