from deprecated.ant import Ant
from deprecated.behaviour_ant import BehaviourAnt
from deprecated.cleaner import Cleaner
from deprecated.forager import Forager
from ant_simulation.actors.modular_ant import ModularAnt
from deprecated.nurse import Nurse
from deprecated.queen import Queen
from deprecated.stigmergy_ant import StigmergyAnt
from ant_simulation.grounds.forage_grounds import ForageGrounds
from ant_simulation.grounds.nest import Nest
from ant_simulation.grounds.tunnel import Tunnel
from ant_simulation.grounds.wall import Wall
from ant_simulation.objects.food import Food
from ant_simulation.objects.test_objects import TestObject
from architecture.generation import factory


def register():
    factory.register_actor(Ant.get_id(), Ant.create)
    factory.register_actor(Nurse.get_id(), BehaviourAnt.create)
    factory.register_actor(Forager.get_id(), BehaviourAnt.create)
    factory.register_actor(Queen.get_id(), BehaviourAnt.create)
    factory.register_actor(Cleaner.get_id(), BehaviourAnt.create)
    factory.register_actor(StigmergyAnt.get_id(), StigmergyAnt.create)
    factory.register_actor(BehaviourAnt.get_id(), BehaviourAnt.create)
    factory.register_actor(ModularAnt.get_id(), ModularAnt.create)

    factory.register_ground(Tunnel.get_id(), Tunnel.create)
    factory.register_ground(Nest.get_id(), Nest.create)
    factory.register_ground(ForageGrounds.get_id(), ForageGrounds.create)
    factory.register_ground(Wall.get_id(), Wall.create)

    factory.register_object(Food.get_id(), Food.create)
    factory.register_object(TestObject.get_id(), TestObject.create)
