from core.ui.ui_element import UIElement
from core.vector import Vector


class Image(UIElement):
    def __init__(self, position=Vector(), size=Vector(), sprite=None, **kwargs):
        super().__init__(position, size, sprite)

