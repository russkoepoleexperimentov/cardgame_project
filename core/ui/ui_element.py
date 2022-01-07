import pygame

from core.game_object import GameObject
from core.ui import ui_manager
from core.vector import Vector


class UIElement(GameObject):
    def __init__(self, position=Vector(), size=Vector(), sprite=None):
        super().__init__(position, size, sprite)
        self.block_raycasts = True

    def update_ui_selected(self):
        if self.block_raycasts:
            mouse_pos = pygame.mouse.get_pos()
            if self.get_rect().collidepoint(mouse_pos):
                ui_manager.set_selected(self)
