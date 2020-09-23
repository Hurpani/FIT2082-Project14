from ant_simulation.behaviours.behaviour import Behaviour
from ant_simulation.behaviours.wander_pheromone_behaviour import WanderPheromoneBehaviour
from ant_simulation.objects.test_objects import TestObject
from architecture.actor import Actor
from architecture.kinds import Kind
from architecture.location import Location
from architecture.position import Position
from architecture.rendering.colour import Colour
from architecture.world import World

class ModularAnt(Actor):
    COLOUR: Colour = Colour(255, 255, 0)
    ID: str = "mant"

    @staticmethod
    def create(kinds: [Kind] = []) -> Actor:
        return ModularAnt(kinds)

    @staticmethod
    def get_id() -> str:
        return ModularAnt.ID

    def get_colour(self) -> Colour:
        return ModularAnt.COLOUR

    def move(self, frm: Location, to: Location):
        to.set_actor(self)
        frm.remove_actor()

    def tick(self, world: World, elapsed: float, location: Location, position: Position):
        self.current_behaviour.do(world, elapsed, location, position, self)
        # TODO : Change these floating literal.
        location.add_pheromones(1)
        location.add_object(TestObject())

    def __init__(self, kinds: [Kind]):
        super().__init__(kinds)
        # TODO : Change this floating literal.
        #                                                            bias, variation, wobble
        self.current_behaviour: Behaviour = WanderPheromoneBehaviour(0.025, 0.2, 0.3)
