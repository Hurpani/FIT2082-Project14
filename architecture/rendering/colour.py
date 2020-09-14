
class Colour:
    """\
        The Colour class. Stores an rgb value for drawing Renderable objects.
    """

    MAX_VALUE: int = 255

    def __init__(self, r: int = 0, g: int = 0, b: int = 0):
        self.r: int = max(min(r, Colour.MAX_VALUE), 0)
        self.g: int = max(min(g, Colour.MAX_VALUE), 0)
        self.b: int = max(min(b, Colour.MAX_VALUE), 0)


    def multiply(self, amount: float):
        return Colour(self.r * amount, self.g * amount, self.b * amount)


    def get_alt_red(self, val: int):
        return Colour(val, self.g, self.b)


    def get_alt_green(self, val: int):
        return Colour(self.r, val, self.b)


    def get_alt_blue(self, val: int):
        return Colour(self.r, self.g, val)


    def get_rgba(self) -> (float, float, float, float):
        """\
    Returns the floating-point rgba 4-tuple representing this colour (fully opaque).
        """
        return ((float(self.r))/Colour.MAX_VALUE, (float(self.g))/Colour.MAX_VALUE, (float(self.b))/Colour.MAX_VALUE, 1.0)
