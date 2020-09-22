from abc import ABC, abstractmethod

from ant_simulation.actors.behaviour_ant import BehaviourAnt
from architecture.location import Location
from architecture.position import Position
from architecture.world import World


class Behaviour(ABC):

    @abstractmethod
    def do(self, world: World, elapsed: float, location: Location, position: Position, ant: BehaviourAnt):
        pass
