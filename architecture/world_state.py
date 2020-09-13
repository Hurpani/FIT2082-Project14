

class WorldState:
    """\
The WorldState object. Contains information informing of current attributes of a World.
    """

    def __init__(self, max_objects_in_location: int):
        self.max_objects_in_location = max_objects_in_location


    def get_max_objects_in_location_count(self):
        return self.max_objects_in_location