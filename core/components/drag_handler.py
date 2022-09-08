import pygame
from core.component import Component
from core.components.drop_handler import DropHandler
from core.action import Action
from core.ui.ui_element import UIElement
from core.ui import ui_manager
from core.vector import Vector
from core.scale_helpers import unscale_vector


class DragHandler(Component):
    def __init__(self, owner: UIElement):
        super(DragHandler, self).__init__(owner)
        self.drag_offset = Vector()
        self.follow_mouse = True

        self.on_begin_drag = Action()
        self.on_drag = Action()
        self.on_end_drag = Action()

    def event_hook(self, event):
        mouse_pos = Vector(*pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if ui_manager.get_selected() == self.get_game_object() and ui_manager.get_dragged() \
                    is None:
                ui_manager.set_dragged(self)
                self.get_game_object().block_raycasts = False
                self.drag_offset = self.get_game_object().scaled_position - mouse_pos
                self.on_begin_drag.invoke()
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
            if ui_manager.get_dragged() == self:
                self.get_game_object().block_raycasts = True
                ui_manager.remove_dragged()

                if ui_manager.get_selected():
                    drop_handler = ui_manager.get_selected().get_component(DropHandler)
                    if drop_handler:
                        drop_handler.process_drop(self)
                self.on_end_drag.invoke()
        if event.type == pygame.MOUSEMOTION:
            if ui_manager.get_dragged() == self:
                if self.follow_mouse:
                    self.get_game_object().scaled_position = mouse_pos + self.drag_offset
                self.on_drag.invoke()


