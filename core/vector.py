class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def xy(self):
        return self.x, self.y


def vector_from_collection(collection):
    if isinstance(collection, (tuple, list)):
        raise TypeError()

    if len(collection) != 2:
        raise Exception()

    return Vector(collection[0], collection[1])
