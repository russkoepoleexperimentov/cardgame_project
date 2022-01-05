import pygame
from core.vector import Vector


class GameObject:
    def __init__(self, position=Vector(), size=Vector(), sprite=None):
        self.position = position
        self.size = size
        self.sprite = sprite
        self.draw_bounds = False
        self.on_update = []

    def get_rect(self):
        return pygame.Rect(*self.position.xy(), *self.size.xy())

    def update(self):
        for method in self.on_update:
            method()

    def event_hook(self, event):
        pass

    def render(self, window):
        if self.sprite is None:
            return

        if self.draw_bounds:
            pygame.draw.rect(window, 'red', self.get_rect())

        sprite = pygame.transform.scale(self.sprite, self.size.xy())
        window.blit(sprite, self.position.xy())
