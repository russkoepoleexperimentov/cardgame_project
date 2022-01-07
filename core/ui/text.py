import pygame

from core.ui.ui_element import UIElement
from core.vector import Vector


class Text(UIElement):
    def __init__(self, position=Vector(), size=Vector(), title='', font=None,
                 color=pygame.Color('white'), align='left', valign='top'):
        super().__init__(position, size, None)
        self.font = font if font is not None else pygame.font.Font(None, 30)
        self.color = color
        self.block_raycasts = False

        self.__title = title
        self.__rendered_title = None
        self.__rect = None
        self.__align = align
        self.__valign = valign

        self.render_title()

    def set_title(self, title):
        self.__title = title
        self.render_title()

    def get_title(self):
        return self.__title

    def set_align(self, align):
        self.__align = align
        self.render_title()

    def get_align(self):
        return self.__align

    def set_valign(self, valign):
        self.__valign = valign
        self.render_title()

    def get_valign(self):
        return self.__valign

    def render_title(self):
        self.__rendered_title = self.font.render(self.__title, True, self.color)
        self.__rect = self.__rendered_title.get_rect()

    def render(self, window):
        super(Text, self).render(window)
        rect = self.__rect.copy()

        if self.__align == 'left':
            rect.left = self.get_rect().left
        elif self.__align == 'right':
            rect.right = self.get_rect().right
        elif self.__align == 'center':
            rect.centerx = self.get_rect().centerx

        if self.__valign == 'top':
            rect.top = self.get_rect().top
        elif self.__valign == 'bottom':
            rect.bottom = self.get_rect().bottom
        elif self.__valign == 'middle':
            rect.centery = self.get_rect().centery

        window.blit(self.__rendered_title, rect)
