import pygame
from core.resources import load_image
from core.rendering.renderer import on_render
from core.vector import Vector
from core.scale_helpers import scale_vector

__initialized = False
CURSOR_SIZE = Vector(24, 24)
cursor_img = load_image('sprites/ui/cursor_small.png')

_last_mouse_pos = (0, 0)


def _redraw_request(rect):
    from core.application import Application
    Application.get().redraw_request(rect)


def draw_cursor(window):
    global _last_mouse_pos
    cursor_sprite = pygame.transform.scale(cursor_img, CURSOR_SIZE.xy())
    _redraw_request((_last_mouse_pos, cursor_sprite.get_size()))
    _last_mouse_pos = pygame.mouse.get_pos()
    window.blit(cursor_sprite, _last_mouse_pos)
    _redraw_request((_last_mouse_pos, cursor_sprite.get_size()))


def init():
    global __initialized
    if __initialized:
        return None
    __initialized = True
    pygame.mouse.set_visible(False)
    on_render.add_listener(draw_cursor)