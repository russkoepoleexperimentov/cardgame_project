import pygame
from core.vector import Vector

class GameObject:
    def __init__(self):
        self.position = Vector(0, 0)
        self.size = Vector(0, 0)

    def render(self, window):
        pygame.draw.rect(window, 'red', (*self.position.xy(), *self.size.xy()))
