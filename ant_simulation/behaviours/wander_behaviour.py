from ant_simulation.actors.behaviour_ant import BehaviourAnt
from ant_simulation.behaviours.behaviour import Behaviour
from architecture.location import Location
from architecture.position import Position
from architecture.world import World


class WanderBehaviour(Behaviour):

    DEFAULT_VARIATION_CHANCE: float = 0.1
    DEFAULT_WOBBLE_CHANCE: float = 0.35

    def __init__(self, pheromone_bias: float = 0, variation_chance: float = DEFAULT_VARIATION_CHANCE, wobble_chance: float = DEFAULT_WOBBLE_CHANCE):
        self.variation_chance: float = variation_chance
        self.wobble_chance: float =  wobble_chance
        self.pheromone_bias: float = pheromone_bias

    def do(self, world: World, elapsed: float, location: Location, position: Position, ant: BehaviourAnt):
        pass
