from core.component import Component
from core.ui.ui_element import UIElement
from core.vector import Vector


class LayoutGroup(Component):
    def __init__(self, owner: UIElement):
        super().__init__(owner)
        self.spacing = 0
        owner.on_add_children.add_listener(self.on_add_children)

    def on_add_children(self, other):
        self.refresh()

    def refresh(self):
        raise NotImplementedError()


class VerticalLayoutGroup(LayoutGroup):
    def refresh(self):
        offset = 0
        for child in self.get_game_object().get_children():
            child.position = Vector(0, offset)
            offset += child.get_size().y + self.spacing


class HorizontalLayoutGroup(LayoutGroup):
    def __init__(self, owner: UIElement):
        super(HorizontalLayoutGroup, self).__init__(owner)
        self.anchor = 'left'

    def refresh(self):
        size_x = 0
        for child in self.get_game_object().get_children():
            size_x += child.get_size().x + self.spacing
        else:
            size_x -= self.spacing

        start_pos = Vector()
        if self.anchor == 'left':
            start_pos = Vector()
        elif self.anchor == 'center':
            start_pos = Vector(self.get_game_object().get_size().x // 2 - size_x // 2, 0)

        offset = 0
        for child in self.get_game_object().get_children():
            child.position = start_pos + Vector(offset, 0)
            offset += child.get_size().x + self.spacing


class GridLayoutGroup(LayoutGroup):
    def __init__(self, owner):
        super(GridLayoutGroup, self).__init__(owner)
        self.cell_size = Vector(100, 100)

    def refresh(self):
        columns = max(1, self.get_game_object().get_size().x // self.cell_size.x)
        for i in range(self.get_game_object().child_count()):
            column_count = i % columns
            row_count = i // columns

            item = self.get_game_object().get_child(i)

            item.position = Vector((self.cell_size.x + self.spacing) * column_count,
                                   (self.cell_size.y + self.spacing) * row_count)
            item.set_size(self.cell_size)
