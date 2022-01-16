import pygame

from core.components.drag_handler import DragHandler
from core.ui.image import Image
from core.vector import Vector

MIN_VALUE, MAX_VALUE = 0, 1


def clamp(x, min, max):
    if min > x:
        return min
    if max < x:
        return max
    return x


class Slider(Image):
    def __init__(self, position=Vector(), size=Vector(), background_sprite=None, handle_sprite=None):
        super(Slider, self).__init__(position, size, background_sprite)

        self.scale = 3
        self.__value = 0
        self.handle = Image(size=size, sprite=handle_sprite)
        self.handle.set_parent(self)

        self.__scroll_drag_handler: DragHandler = self.handle.add_component(DragHandler)
        self.__scroll_drag_handler.follow_mouse = False
        self.__scroll_drag_handler.on_begin_drag.add_listener(self.on_begin_drag)
        self.__scroll_drag_handler.on_drag.add_listener(self.on_drag)

        self.__drag_offset = Vector()

    def value(self):
        return self.__value

    def on_begin_drag(self):
        mouse_pos = pygame.mouse.get_pos()
        drag_offset = self.handle.position - Vector(*mouse_pos)
        self.__drag_offset = Vector(0, drag_offset.y)

    def on_drag(self):
        mouse_pos = pygame.mouse.get_pos()
        max_y = self.get_size().y - self.scale
        handle_y = clamp(mouse_pos[1] + self.__drag_offset.y, 0, max_y)
        self.__value = round(handle_y / max_y, 2)
        self.handle.position = Vector(y=handle_y)

    def update(self, delta_time):
        super(Slider, self).update(delta_time)
        self_size = self.get_size()
        self.handle.set_size(Vector(self_size.x, self.scale))
