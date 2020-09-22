##############################
from __future__ import annotations
from typing import TYPE_CHECKING
##############################

if TYPE_CHECKING:
    from ant_simulation.actors.behaviour_ant import BehaviourAnt

from abc import ABC, abstractmethod
from architecture.location import Location
from architecture.position import Position
from architecture.world import World


class Behaviour(ABC):

    @abstractmethod
    def do(self, world: World, elapsed: float, location: Location, position: Position, ant: BehaviourAnt):
        pass
