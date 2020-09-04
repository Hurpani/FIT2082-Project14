

class InvalidIdException(Exception):
    """\
The InvalidIdException class. This exception is raised when either an
    id is already taken when registering an Actor or Ground in
    the factory, or if no such id is found for calling.
    """
    pass
