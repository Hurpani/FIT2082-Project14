from ant_simulation.actors.modular_ant import ModularAnt
from architecture.generation.world_builder import create_world
from architecture.world import World


def save(world: World):
    world.write_out()
    ModularAnt.save_interactions()

def load(grounds_file: str, actors_file: str, objects_file: str = None) -> World:
    world: World = create_world(grounds_file, World.WRITE_OUT_FILE_PATH / actors_file,
                                World.WRITE_OUT_FILE_PATH / objects_file if objects_file is not None else None)
    world.restore_pheromones()
    return world
