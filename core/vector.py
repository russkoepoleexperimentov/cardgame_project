class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def xy(self):
        return self.x, self.y

    def xo(self):
        return Vector(self.x, 0)

    def oy(self):
        return Vector(0, self.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other: int):
        return Vector(self.x * other, self.y * other)

    def __imul__(self, other: int):
        return self.__mul__(other)
