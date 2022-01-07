import pygame
from core.component import Component
from core.action import Action
from core.ui.ui_element import UIElement
from core.ui import ui_manager
from core.vector import Vector


class DragHandler(Component):
    def __init__(self, owner: UIElement):
        super(DragHandler, self).__init__(owner)
        self.mouse_over_down = False
        self.drag_offset = Vector()
        self.on_begin_drag = Action()
        self.on_end_drag = Action()

    def event_hook(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if ui_manager.get_selected() == self.get_game_object():
                self.mouse_over_down = True
                self.get_game_object().block_raycasts = False
                self.drag_offset = self.get_game_object().position - Vector(*mouse_pos)
                self.on_begin_drag.invoke()
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if self.mouse_over_down:
                self.on_end_drag.invoke()
                self.get_game_object().block_raycasts = True
                self.mouse_over_down = False
        if event.type == pygame.MOUSEMOTION:
            if self.mouse_over_down:
                self.get_game_object().position = Vector(*mouse_pos) + self.drag_offset


