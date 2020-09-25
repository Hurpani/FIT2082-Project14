from ant_simulation.behaviours.behaviour import Behaviour
from deprecated.wander_behaviour import WanderBehaviour
from architecture.actor import Actor
from architecture.kinds import Kind
from architecture.location import Location
from architecture.object import Object
from architecture.position import Position
from architecture.rendering.colour import Colour
from architecture.world import World
from ant_simulation.objects.test_objects import TestObject

import random

class BehaviourAnt(Actor):

    age: float = 0
    COLOUR: Colour = Colour(255, 255, 0)
    ID: str = "bant"
    DROP_CHANCE: float = 0.5

    @staticmethod
    def create(kinds: [Kind] = []) -> Actor:
        return BehaviourAnt(kinds)

    @staticmethod
    def get_id() -> str:
        return BehaviourAnt.ID

    def get_colour(self) -> Colour:
        if self.age > 200:
            return Colour(255,255,0)
        else:
            return Colour(255,self.age,255-self.age)

    def move(self, frm: Location, to: Location):
        to.set_actor(self)
        frm.remove_actor()


    def tick(self, world: World, elapsed: float, location: Location, position: Position):
        self.current_behaviour: Behaviour = WanderBehaviour(0,1-(self.age/300),1-(self.age/600))
        self.current_behaviour.do(world, elapsed, location, position, self)
        location.add_object(TestObject())
        self.age += 0.1 * elapsed


    def __init__(self, kinds: [Kind]):
        super().__init__(kinds)
        self.carrying: Object = None
        self.current_behaviour: Behaviour = WanderBehaviour()
        self.previous_behaviour: Behaviour = WanderBehaviour()
        self.age = 200 * random.random()
        self.current_dir = random.choice([[-1, -1], [-1, 0], [0, -1], [1, 1], [1, 0], [0, 1], [-1, 1], [1, -1]])
