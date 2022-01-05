from core.vector import Vector
from core.ui.ui_element import UIElement


class VerticalLayoutGroup:
    def __init__(self, start_position=Vector(), spacing=0):
        self.start_position = start_position
        self.spacing = spacing
        self.elements = []

    def add(self, ui_element: UIElement):
        self.elements.append(ui_element)
        self.refresh()

    def refresh(self):
        step = 0
        for elem in self.elements:
            elem.position = self.start_position + Vector(0, step)
            step += elem.size.y + self.spacing
