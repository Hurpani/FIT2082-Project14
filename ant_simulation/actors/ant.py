from ant_simulation.objects.test_objects import TestObject
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

    DIRECTION_CHANGE_CHANCE: float = 0.4

    @staticmethod
    def create(kinds: [Kind] = []) -> Actor:
        return Ant(kinds)


    @staticmethod
    def get_id() -> str:
        return "ant"


    def get_kinds(self) -> [Kind]:
        return self.kinds


    def tick(self, world: World, elapsed: float, location: Location, pos: Position):
        #self.change_dir_random(world,elapsed,location,pos)
        self.change_dir_random_chance(world,elapsed,location,pos, Ant.DIRECTION_CHANGE_CHANCE)

    def change_dir_random(self, world: World, elapsed: float, location: Location, pos: Position):
        possible_free_locations = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 and j != 0:
                    if world.get_location(pos.get_coordinates()[0] + i, pos.get_coordinates()[1] + j).is_free():
                        possible_free_locations.append([pos.get_coordinates()[0] + i, pos.get_coordinates()[1] + j, i, j])
        if len(possible_free_locations) > 0:
            random_avalible_space = random.choice(possible_free_locations)
            world.get_location(pos.get_coordinates()[0], pos.get_coordinates()[1]).remove_actor()
            world.get_location(random_avalible_space[0], random_avalible_space[1]).set_actor(self)

            world.get_location(random_avalible_space[0], random_avalible_space[1]).add_object(TestObject())

            self.current_dir = [random_avalible_space[2],random_avalible_space[3]]

    def change_dir_random_chance(self, world: World, elapsed: float, location: Location, pos: Position, chance: float):
        if  chance < random.random():
            if world.get_location(pos.get_coordinates()[0] + self.current_dir[0], pos.get_coordinates()[1] + self.current_dir[1]).is_free() and random.random() > 0.5:
                    world.get_location(pos.get_coordinates()[0], pos.get_coordinates()[1]).remove_actor()
                    world.get_location(pos.get_coordinates()[0] + self.current_dir[0], pos.get_coordinates()[1] + self.current_dir[1]).set_actor(self)

                    # temporary adding of test object.
                    world.get_location(pos.get_coordinates()[0] + self.current_dir[0], pos.get_coordinates()[1] + self.current_dir[1]).add_object(TestObject())
                    # end.
            else:
                next_dirr = self.give_dir_next_to_current( self.current_dir[0], self.current_dir[1])
                if world.get_location(pos.get_coordinates()[0] + next_dirr[0][0],pos.get_coordinates()[1] + next_dirr[0][1]).is_free():
                    world.get_location(pos.get_coordinates()[0], pos.get_coordinates()[1]).remove_actor()
                    world.get_location(pos.get_coordinates()[0] + next_dirr[0][0], pos.get_coordinates()[1] + next_dirr[0][1]).set_actor(self)

                    # temporary adding of test object.
                    world.get_location(pos.get_coordinates()[0] + next_dirr[0][0], pos.get_coordinates()[1] + next_dirr[0][1]).add_object(TestObject())
                    # end.

                elif world.get_location(pos.get_coordinates()[0] + next_dirr[1][0],pos.get_coordinates()[1] + next_dirr[1][1]).is_free():
                    world.get_location(pos.get_coordinates()[0], pos.get_coordinates()[1]).remove_actor()
                    world.get_location(pos.get_coordinates()[0] + next_dirr[1][0], pos.get_coordinates()[1] + next_dirr[1][1]).set_actor(self)

                    # temporary adding of test object.
                    world.get_location(pos.get_coordinates()[0] + next_dirr[1][0], pos.get_coordinates()[1] + next_dirr[1][1]).add_object(TestObject())
                    # end.

                else:
                    self.change_dir_random(world,elapsed,location,pos)
        else:
            self.change_dir_random(world,elapsed,location,pos)


    def add_kind(self, kind: Kind):
        self.kinds.append(kind)

    def get_colour(self) -> Colour:
        return Colour()

    def give_dir_next_to_current(self,i,j):
        if i == -1 and j == 1:
            if random.random() > 0.5:
                return([[-1,0],[0,1]])
            return ([[0, 1],[-1, 0]])
        if i == -1 and j == 0:
            if random.random() > 0.5:
                return([[-1,1],[-1,-1]])
            return([[-1,-1],[-1,1]])
        if i == -1 and j == -1:
            if random.random() > 0.5:
                return([[-1,0],[0,-1]])
            return([[0,-1],[-1,0]])
        if i == 0 and j == 1:
            if random.random() > 0.5:
                return([[-1,1],[1,1]])
            return ([[1, 1], [-1, 1]])
        if i == 0 and j == -1:
            if random.random() > 0.5:
                return([[-1,-1],[1,-1]])
            return ([[1,-1], [-1,-1]])
        if i == 1 and j == 1:
            if random.random() > 0.5:
                return([[0,1],[1,0]])
            return([[1,0],[0,1]])
        if i == 1 and j == 0:
            if random.random() > 0.5:
                return([[1,1],[1,-1]])
            return([[1,-1],[1,1]])
        if i == 1 and j == -1:
            if random.random() > 0.5:
                return([[1,0],[0,-1]])
            return([[0,-1],[1,0]])

    def __init__(self, kinds: [Kind]):
        super().__init__(kinds)
        self.current_dir = random.choice([[-1,-1],[-1,0],[0,-1],[1,1],[1,0],[0,1],[-1,1],[1,-1]])







