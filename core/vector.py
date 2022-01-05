class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def xy(self):
        return self.x, self.y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        return self.__add__(other)

    def __mul__(self, other: int):
        return Vector(self.x * other, self.y * other)

    def __imul__(self, other):
        return self.__mul__(other)


def vector_from_collection(collection):
    if isinstance(collection, (tuple, list)):
        raise TypeError()

    if len(collection) != 2:
        raise Exception()

    return Vector(collection[0], collection[1])
