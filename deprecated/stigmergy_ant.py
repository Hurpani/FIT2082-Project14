from random import Random

from ant_simulation.objects.test_objects import TestObject
from architecture.actor import Actor
from architecture.kinds import Kind
from architecture.location import Location
from architecture.object import Object
from architecture.position import Position
from architecture.rendering.colour import Colour
from architecture.world import World


class StigmergyAnt(Actor):

    COLOUR: Colour = Colour(255, 255, 0)
    ALT_COLOUR: Colour = Colour(255, 128, 0)
    ID: str = "sant"
    DROP_CHANCE: float = 0.5

    @staticmethod
    def create(kinds: [Kind] = []) -> Actor:
        return StigmergyAnt(kinds)

    @staticmethod
    def get_id() -> str:
        return StigmergyAnt.ID

    def get_colour(self) -> Colour:
        return StigmergyAnt.COLOUR if self.carrying is None else StigmergyAnt.ALT_COLOUR

    def food_interaction(self, loc: Location, world: World, position: Position):
        if self.carrying is not None and Random().random() < StigmergyAnt.DROP_CHANCE:
            for l in world.get_adjacent_locations(position.x, position.y, 1, False):
                if len(l.get_objects(Kind.FOOD)) > 0:
                    loc.add_object(self.carrying)
                    self.carrying = None
                    break
        else:
            food_items: [Object] = loc.get_objects(Kind.FOOD)
            if len(food_items) > 0:
                    self.carrying = food_items[0]
                    loc.remove_object(self.carrying)

    def move(self, frm: Location, to: Location):
        to.set_actor(self)
        to.add_object(TestObject())
        frm.remove_actor()

    def tick(self, world: World, elapsed: float, location: Location, position: Position):
        try:
            # COMPLETELY RANDOM CHOICES FOR WALKS (no preserving of direction).
            to: Location = Random().choice(world.get_adjacent_locations(position.x, position.y, 1, True))
            self.move(location, to)
            self.food_interaction(to, world, position)
        except IndexError:
            # The ant can't find anywhere to move...
            location.add_object(TestObject())

    def __init__(self, kinds: [Kind]):
        super().__init__(kinds)
        self.carrying: Object = None
