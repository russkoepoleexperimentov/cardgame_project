from core.vector import Vector
from core.game_object import GameObject


class LayoutGroup(GameObject):
    def __init__(self, position=Vector(), size=Vector(), spacing=0):
        super().__init__(position, size, None)
        self.spacing = spacing

    def on_add_children(self, other):
        self.refresh()

    def refresh(self):
        raise NotImplementedError()


class VerticalLayoutGroup(LayoutGroup):
    def refresh(self):
        offset = 0
        for child in self.get_children():
            child.position = Vector(0, offset)
            offset += child.size.y + self.spacing


class HorizontalLayoutGroup(LayoutGroup):
    def refresh(self):
        offset = 0
        for child in self.get_children():
            child.position = Vector(offset, 0)
            offset += child.size.x + self.spacing
