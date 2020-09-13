
class Colour:
    """\
        The Colour class. Stores an rgb value for drawing Renderable objects.
    """

    MAX_VALUE: int = 255

    def __init__(self, r: int = 0, g: int = 0, b: int = 0):
        if 0 <= r <= Colour.MAX_VALUE and 0 <= g <= Colour.MAX_VALUE and 0 <= b <= Colour.MAX_VALUE:
            self.r: int = r
            self.g: int = g
            self.b: int = b
        else:
            raise ValueError()


    def multiply(self, amount: float):
        return Colour(self.r * amount, self.g * amount, self.b * amount)


    def get_rgba(self) -> (float, float, float, float):
        """\
    Returns the floating-point rgba 4-tuple representing this colour (fully opaque).
        """
        return ((float(self.r))/Colour.MAX_VALUE, (float(self.g))/Colour.MAX_VALUE, (float(self.b))/Colour.MAX_VALUE, 1.0)
