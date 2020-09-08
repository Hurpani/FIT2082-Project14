from architecture.generation import factory
from architecture.location import Location
from architecture.world import World

# TODO : Support "kinds".


def __generate_with_grounds(grounds_file: str) -> World:
    with open(grounds_file) as file:
        lines: [str] = file.readlines()
        width, height = int(lines[0].split()[0]), int(lines[0].split()[1])
        world = World(width, height)

        for y in range(height):
            strings = lines[y + 1].split()
            for x in range(width):
                world.set_location(Location(factory.make_ground(strings[x])), x, y)
        return world


def __populate_with_actors(world: World, actors_file: str) -> World:
    if actors_file is None or actors_file == "":
        return world
    with open(actors_file) as file:
        lines: [str] = file.readlines()
        for line in lines:
            name, x, y = line.split()[0], int(line.split()[1]), int(line.split()[2])
            world.add_actor(factory.make_actor(name), x, y)
    return world


def __populate_with_objects(world: World, objects_file: str) -> World:
    if objects_file is None or objects_file == "":
        return world

    # TODO.

    return world


def create_world(grounds_file: str, actors_file: str, objects_file: str) -> World:
    return __populate_with_objects(__populate_with_actors(
        __generate_with_grounds(grounds_file), actors_file), objects_file)

