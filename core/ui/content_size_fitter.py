from core.component import Component
from core.ui.ui_element import UIElement
from core.vector import Vector


class ContentSizeFitter(Component):
    def __init__(self, owner: UIElement):
        super(ContentSizeFitter, self).__init__(owner)
        self.after_space = 10
        owner.on_add_children.add_listener(self.on_add_children)

    def on_add_children(self, other):
        self.refresh()

    def refresh(self):
        pass


class VerticalContentSizeFitter(ContentSizeFitter):
    def refresh(self):
        children = self.get_game_object().get_children()
        if len(children) < 1:
            return None
        sorted_children = sorted(children, key=lambda x: x.position.y, reverse=True)
        lower_children = sorted_children[0]

        size = self.get_game_object().get_size()
        self.get_game_object().set_size(Vector(size.x, lower_children.position.y +
                                               lower_children.get_size().y + self.after_space))
