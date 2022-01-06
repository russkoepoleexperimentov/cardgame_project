import pygame

from core.ui.ui_element import UIElement
from core.vector import Vector


class Text(UIElement):
    def __init__(self, position=Vector(), size=Vector(), title='', font=None,
                 color=pygame.Color('white')):
        super().__init__(position, size, None)
        self.title = title
        self.font = font if font is not None else pygame.font.Font(None, 30)
        self.color = color
        self.h_alignment = 'left'
        self.block_raycasts = False

    def render(self, window):
        rendered_font = self.font.render(self.title, True, self.color)
        render_kwargs = {
            'center': (self.size * 0.5).xy()
        }
        rect = rendered_font.get_rect(**render_kwargs)
        rect.x += self.get_global_position().x
        rect.y += self.get_global_position().y
        window.blit(rendered_font, rect)
