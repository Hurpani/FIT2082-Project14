from ant_simulation.actors.ant import Ant
from architecture.actor import Actor
from architecture.kinds import Kind
from architecture.location import Location
from architecture.position import Position
from architecture.rendering.colour import Colour
from architecture.world import World
import random

class Queen(Ant):
    ID: str = "Queen"
    COLOUR: Colour = Colour(75, 0, 130)

    @staticmethod
    def create(kinds: [Kind] = []) -> Actor:
        return Queen(kinds)

    @staticmethod
    def get_id() -> str:
        return Queen.ID

    def tick(self, world: World, elapsed: float, location: Location, pos: Position):
        possible_free_locations = []
        for i in range(-1,2):
            for j in range(-1,2):
                if i != 0 and j != 0:
                    try:
                        if world.get_location(pos.get_coordinates()[0]+i, pos.get_coordinates()[1]+j).is_free():
                            possible_free_locations.append([pos.get_coordinates()[0]+i,pos.get_coordinates()[1]+j])
                    except:
                        pass
        if len(possible_free_locations) > 0:
            random_avalible_space = random.choice(possible_free_locations)
            #print(random_avalible_space)



    @staticmethod
    def get_colour() -> Colour:
        return Queen.COLOUR

    def __init__(self, kinds: [Kind]):
        super().__init__(kinds)