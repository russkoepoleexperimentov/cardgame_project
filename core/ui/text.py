import pygame

from core.game_object import GameObject
from core.vector import Vector


class Text(GameObject):
    def __init__(self, position=Vector(), size=Vector(), title='', font=None,
                 color=pygame.Color('white')):
        super().__init__(position, size, None)
        self.title = title
        self.font = font if font is not None else pygame.font.Font(None, 30)
        self.color = color

    def render(self, window):
        rendered_font = self.font.render(self.title, True, self.color)
        window.blit(rendered_font, self.get_rect())
