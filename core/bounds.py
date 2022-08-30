from core.vector import Vector


class Bounds:
    def __init__(self, position=Vector(), size=Vector()):
        self.position = position
        self.size = size

    def inside_parent(self, parent):
        if self.position.x > parent.position.x + parent.size.x:
            return False

        if self.position.y > parent.position.y + parent.size.y:
            return False

        if self.position.x + self.size.x < parent.position.x:
            return False

        if self.position.y + self.size.y < parent.position.y:
            return False

        return True