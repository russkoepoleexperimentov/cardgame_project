class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def xy(self):
        return self.x, self.y

    def yx(self):
        return self.y, self.x
    