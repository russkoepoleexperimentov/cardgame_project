import pygame
from core.game_object import GameObject
from core.vector import Vector, vector_from_collection


class Button(GameObject):
    def __init__(self, position=Vector(), size=Vector(), sprite=None):
        super().__init__(position, size, sprite)
        self.on_click = []

    def event_hook(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.get_rect().collidepoint(mouse_pos):
                for method in self.on_click:
                    method()