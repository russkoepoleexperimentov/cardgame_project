from core.vector import Vector
from core.game_object import GameObject


class VerticalLayoutGroup(GameObject):
    def __init__(self, position=Vector(), size=Vector(), spacing=0):
        super().__init__(position, size, None)
        self.spacing = spacing

    def on_add_children(self, other):
        self.refresh()

    def refresh(self):
        step = 0
        for elem in self.get_children():
            elem.position = Vector(0, step)
            step += elem.size.y + self.spacing

    def render(self, window):
        super().render(window)
