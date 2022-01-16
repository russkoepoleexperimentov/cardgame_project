import pygame

from core.ui.ui_element import UIElement
from core.vector import Vector


class Text(UIElement):
    def __init__(self, position=Vector(), size=Vector(), title='', font_name=None,
                 color=pygame.Color('white'), align='left', valign='top', font_size=30):
        super().__init__(position, size, None)
        self.color = color
        self.block_raycasts = False

        self.__title = title
        self.__rendered_title = None
        self.__rect = None
        self.__align = align
        self.__valign = valign
        self.__font_name = font_name
        self.__font_size = font_size

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

    def set_font_size(self, size):
        self.__font_size = size
        self.render_title()

    def get_font_size(self):
        return self.__font_size

    def set_font(self, font_name):
        self.__font_name = font_name
        self.render_title()

    def get_font(self):
        return self.__font_name

    def render_title(self):
        font = pygame.font.Font(self.__font_name, self.__font_size)
        self.__rendered_title = font.render(self.__title, True, self.color)
        self.__rect = self.__rendered_title.get_rect()

    def render(self, window, offset=Vector(0, 0)):
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

        rect.x -= offset.x
        rect.y -= offset.y

        window.blit(self.__rendered_title, rect)
        super(Text, self).render(window)
