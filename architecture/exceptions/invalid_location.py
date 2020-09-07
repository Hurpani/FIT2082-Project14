

class InvalidLocationException(Exception):
    """\
The InvalidLocationException class. This exception is raised when
    a location already contains an Actor, or when the specified
    coordinates for a Location in a World are out of bounds.
    """
    pass