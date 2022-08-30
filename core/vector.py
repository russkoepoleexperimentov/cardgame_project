import numpy


class Vector:
    def __init__(self, x=0, y=0):
        self._data = numpy.array((x, y), dtype=numpy.float32)

    @property
    def x(self):
        return self._data[0]

    @x.setter
    def x(self, value):
        self._data[0] = value

    @property
    def y(self):
        return self._data[1]

    @y.setter
    def y(self, value):
        self._data[1] = value

    def xy(self):
        return self._data.tolist()

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

    def __mul__(self, other: float):
        return Vector(self.x * other, self.y * other)

    def __imul__(self, other: float):
        return self.__mul__(other)
