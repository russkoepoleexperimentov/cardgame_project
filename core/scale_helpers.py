import pygame.display

from core.vector import Vector

REFERENCE_RESOLUTION_WIDTH = 1366


def get_scale_coefficient():
    return pygame.display.get_window_size()[0] / REFERENCE_RESOLUTION_WIDTH


def scale_vector(vector: Vector):
    x, y = vector.xy()
    x *= get_scale_coefficient()
    y *= get_scale_coefficient()
    return Vector(x, y)


def unscale_vector(vector: Vector):
    x, y = vector.xy()
    x /= get_scale_coefficient()
    y /= get_scale_coefficient()
    return Vector(x, y)
