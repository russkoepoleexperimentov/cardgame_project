import pygame

from core.ui.ui_element import UIElement
from core.vector import Vector


class Text(UIElement):
    def __init__(self, position=Vector(), size=Vector(), title='', font=None,
                 color=pygame.Color('white'), anchor='topleft'):
        super().__init__(position, size, None)
        self.font = font if font is not None else pygame.font.Font(None, 30)
        self.color = color
        self.block_raycasts = False

        self.__title = title
        self.__rendered_title = None
        self.__rect = None
        self.__anchor = anchor

        self.render_title()

    def set_title(self, title):
        self.__title = title
        self.render_title()

    def get_title(self):
        return self.__title

    def set_anchor(self, anchor):
        self.__anchor = anchor
        self.render_title()

    def get_anchor(self):
        return self.__anchor

    def render_title(self):
        self.__rendered_title = self.font.render(self.__title, True, self.color)
        self.__rect = self.__rendered_title.get_rect()
        setattr(self.__rect, self.__anchor, self.position.xy())

    def render(self, window):
        rect = self.__rect.copy()
        rect.x += (self.get_global_position() - self.position).x
        rect.y += (self.get_global_position() - self.position).y
        window.blit(self.__rendered_title, rect)
