from core.action import Action
from core.component import Component
from core.ui.ui_element import UIElement


class DropHandler(Component):
    def __init__(self, owner: UIElement):
        super(DropHandler, self).__init__(owner)
        self.on_drop = Action()

    def process_drop(self, drag_handler):
        self.on_drop.invoke(drag_handler)
