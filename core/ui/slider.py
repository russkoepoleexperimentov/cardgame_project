import pygame

from core.action import Action
from core.components.drag_handler import DragHandler
from core.ui import ui_manager
from core.ui.image import Image
from core.vector import Vector

MIN_VALUE, MAX_VALUE = 0, 1

MOUSE_WHEEL_SENSETIVITY = 0.1


def clamp(x, min, max):
    if min > x:
        return min
    if max < x:
        return max
    return x


class Slider(Image):
    def __init__(self, position=Vector(), size=Vector(), background_sprite=None, handle_sprite=None):
        super(Slider, self).__init__(position, size, background_sprite)

        self.on_value_changed = Action()

        self.__scale = 3
        self.__value = 0
        self.handle = Image(size=size, sprite=handle_sprite)
        self.handle.set_parent(self)

        self.__scroll_drag_handler: DragHandler = self.handle.add_component(DragHandler)
        self.__scroll_drag_handler.follow_mouse = False
        self.__scroll_drag_handler.on_begin_drag.add_listener(self.on_begin_drag)
        self.__scroll_drag_handler.on_drag.add_listener(self.on_drag)

        self.__drag_offset = Vector()

    def set_value(self, value):
        value = clamp(value, 0, 1)
        max_y = self.get_size().y - self.__scale
        y_pos = value * max_y
        self.handle.position = Vector(y=y_pos)
        self.__value = value
        self.on_value_changed.invoke(self.__value)

    def get_value(self):
        return self.__value

    def set_scale(self, scale):
        self.handle.set_size(Vector(self.get_size().x, min(self.get_size().y, scale)))
        self.__scale = scale

    def get_scale(self):
        return self.__scale

    def on_begin_drag(self):
        mouse_pos = pygame.mouse.get_pos()
        drag_offset = self.handle.position - Vector(*mouse_pos)
        self.__drag_offset = Vector(0, drag_offset.y)

    def on_drag(self):
        mouse_pos = pygame.mouse.get_pos()
        max_y = self.get_size().y - self.__scale

        if self.__scale >= max_y:
            return None

        handle_y = clamp(mouse_pos[1] + self.__drag_offset.y, 0, max_y)
        self.__value = round(handle_y / max_y, 2)
        self.on_value_changed.invoke(self.__value)
        self.handle.position = Vector(y=handle_y)

    def event_hook(self, event):
        super().event_hook(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if ui_manager.get_selected() in (self, self.handle):
                if event.button == 4:
                    self.set_value(self.get_value() - MOUSE_WHEEL_SENSETIVITY)
                elif event.button == 5:
                    self.set_value(self.get_value() + MOUSE_WHEEL_SENSETIVITY)
