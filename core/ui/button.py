import pygame
from core.ui import ui_manager
from core.ui.ui_element import UIElement
from core.ui.text import Text
from core.vector import Vector


class Button(UIElement):
    def __init__(self, position=Vector(), size=Vector(), sprite=None, title=''):
        super().__init__(position, size, sprite)
        self.on_click = []
        self.label = Text(size=size)
        self.label.set_parent(self)
        self.set_title(title)

    def event_hook(self, event):
        super().event_hook(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if ui_manager.get_selected() == self:
                for method in self.on_click:
                    method()

    def set_title(self, title=''):
        self.label.size = self.size
        self.label.title = title

