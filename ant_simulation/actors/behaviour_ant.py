from ant_simulation.behaviours.behaviour import Behaviour
from ant_simulation.behaviours.wander_behaviour import WanderBehaviour
from architecture.actor import Actor
from architecture.kinds import Kind
from architecture.location import Location
from architecture.object import Object
from architecture.position import Position
from architecture.rendering.colour import Colour
from architecture.world import World


class BehaviourAnt(Actor):

    COLOUR: Colour = Colour(255, 255, 0)
    ALT_COLOUR: Colour = Colour(255, 128, 0)
    ID: str = "bant"
    DROP_CHANCE: float = 0.5

    @staticmethod
    def create(kinds: [Kind] = []) -> Actor:
        return BehaviourAnt(kinds)

    @staticmethod
    def get_id() -> str:
        return BehaviourAnt.ID

    def get_colour(self) -> Colour:
        return BehaviourAnt.COLOUR if self.carrying is None else BehaviourAnt.ALT_COLOUR

    def move(self, frm: Location, to: Location):
        to.set_actor(self)
        frm.remove_actor()

    def tick(self, world: World, elapsed: float, location: Location, position: Position):
        self.current_behaviour.do(world, location, position, self)

    def __init__(self, kinds: [Kind]):
        super().__init__(kinds)
        self.carrying: Object = None
        self.current_behaviour: Behaviour = WanderBehaviour()
        self.previous_behaviour: Behaviour = WanderBehaviour()
