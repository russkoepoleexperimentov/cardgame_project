import pygame
from core.resources import load_image
from core.rendering.renderer import on_render
from core.vector import Vector

__initialized = False
CURSOR_SIZE = Vector(24, 24)
cursor_img = load_image('sprites/ui/cursor_small.png')


def draw_cursor(window):
    cursor_sprite = pygame.transform.scale(cursor_img, CURSOR_SIZE.xy())
    mouse_pos = pygame.mouse.get_pos()
    window.blit(cursor_sprite, mouse_pos)


def init():
    global __initialized
    if __initialized:
        return None
    __initialized = True
    pygame.mouse.set_visible(False)
    on_render.add_listener(draw_cursor)