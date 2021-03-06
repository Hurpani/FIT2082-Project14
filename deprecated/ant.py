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

    DIRECTION_CHANGE_CHANCE: float = 0.2

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

    def move_ant(self,world: World, elapsed: float, pos: Position, target:list):
        world.get_location(pos.get_coordinates()[0], pos.get_coordinates()[1]).remove_actor()
        world.get_location(target[0], target[1]).set_actor(self)
        world.get_location(target[0], target[1]).add_object(TestObject())

    def change_dir_random(self, world: World, elapsed: float, location: Location, pos: Position):
        possible_free_locations = []
        #scan 1 range saving taking note of all available spots
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 and j != 0:
                    if world.get_location(pos.get_coordinates()[0] + i, pos.get_coordinates()[1] + j).is_free():
                        possible_free_locations.append([pos.get_coordinates()[0] + i, pos.get_coordinates()[1] + j, i, j])
        #if atleast 1 available spot in 1 range
        if len(possible_free_locations) > 0:
            #pick a random one and move there
            random_available_space = random.choice(possible_free_locations)
            self.move_ant(world,elapsed,pos,random_available_space)
            self.current_dir = [random_available_space[2],random_available_space[3]]

    def change_dir_random_chance(self, world: World, elapsed: float, location: Location, pos: Position, chance: float):
        if  chance < random.random(): #90% of the time

            #if spot in same direction is free and passes a 33% chance, go there
            if world.get_location(pos.get_coordinates()[0] + self.current_dir[0], pos.get_coordinates()[1] + self.current_dir[1]).is_free() and random.random() < 1/3:
                self.move_ant(world, elapsed, pos, [pos.get_coordinates()[0] + self.current_dir[0], pos.get_coordinates()[1] + self.current_dir[1]])
            else:
                #with a 50% choose the adjacent spot e.g. if going north, pick north-east 50% of the time , north-west 50% of the time
                next_dirr = self.give_dir_next_to_current( self.current_dir[0], self.current_dir[1])

                #if the first picked adjacent spot is free go there
                if world.get_location(pos.get_coordinates()[0] + next_dirr[0][0],pos.get_coordinates()[1] + next_dirr[0][1]).is_free():
                    self.move_ant(world, elapsed, pos, [pos.get_coordinates()[0] + next_dirr[0][0], pos.get_coordinates()[1] + next_dirr[0][1]])

                # else if the second picked adjacent spot is free go there
                elif world.get_location(pos.get_coordinates()[0] + next_dirr[1][0],pos.get_coordinates()[1] + next_dirr[1][1]).is_free():
                    self.move_ant(world, elapsed, pos, [pos.get_coordinates()[0] + next_dirr[1][0], pos.get_coordinates()[1] + next_dirr[1][1]])

                #else go random available spot ... and if no spot available change_dir_random will make the ant stay still
                else:
                    self.change_dir_random(world,elapsed,location,pos)

        else: #10% of the time go random available spot ... and if no spot available change_dir_random will make the ant stay still
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







