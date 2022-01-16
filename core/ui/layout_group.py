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
            offset += child.get_size().y + self.spacing


class HorizontalLayoutGroup(LayoutGroup):
    def refresh(self):
        offset = 0
        for child in self.get_children():
            child.position = Vector(offset, 0)
            offset += child.get_size().x + self.spacing


class GridLayoutGroup(LayoutGroup):
    def __init__(self, position=Vector(), size=Vector(), spacing=0, cell_size=Vector(100, 100)):
        super(GridLayoutGroup, self).__init__(position, size, spacing)
        self.cell_size = cell_size

    def refresh(self):
        columns = max(1, self.get_size().x // (self.cell_size.x + self.spacing))
        for i in range(self.child_count()):
            column_count = i % columns
            row_count = i // columns

            item = self.get_child(i)

            item.position = Vector((self.cell_size.x + self.spacing) * column_count,
                                   (self.cell_size.y + self.spacing) * row_count)
            item.set_size(self.cell_size)
