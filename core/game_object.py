import pygame

from core.action import Action
from core.vector import Vector
from core.component import Component
from core.scale_helpers import *


class GameObject:
    @staticmethod
    def redraw_request(rect):
        from core.application import Application
        Application.get().redraw_request(rect)

    def __init__(self, position=Vector(), size=Vector(), sprite=None):
        self._enabled = True
        self.draw_bounds = False

        self.__components = []
        self.__parent = None
        self.__children = []

        self.on_add_children = Action()

        self._position = None
        self.__size = None
        self.__sprite = None

        self.position = position
        self.size = size
        self.sprite = sprite

        self.send_redraw_request()

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value
        self.send_redraw_request()

    @property
    def position(self):
        return self._position

    @property
    def scaled_position(self):
        return scale_vector(self._position)

    @position.setter
    def position(self, value):
        self.send_redraw_request()
        self._position = value
        self.send_redraw_request()

    @property
    def global_position(self):
        return unscale_vector(self.scaled_global_position())

    @property
    def scaled_global_position(self):
        if self.__parent is None:
            return self.scaled_position
        else:
            return self.__parent.scaled_global_position + self.scaled_position

    @property
    def sprite(self):
        return self.__sprite

    @sprite.setter
    def sprite(self, sprite):
        if sprite:
            self.__sprite = pygame.transform.scale(sprite, self.scaled_size.xy()).convert_alpha()
        else:
            self.__sprite = None
        self.send_redraw_request()

    @property
    def size(self):
        return self.__size

    @property
    def scaled_size(self):
        return scale_vector(self.__size)

    @size.setter
    def size(self, size):
        self.send_redraw_request()
        self.__size = size
        self.send_redraw_request()
        self.set_sprite(self.__sprite)

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, other):
        self._set_parent_with_sibling_index(other, -1)

    def send_redraw_request(self):
        if self.position and self.size:
            GameObject.redraw_request((*self.scaled_position.xy(), *self.scaled_size.xy()))

    def _set_parent_with_sibling_index(self, other, sibling_index=-1):
        if self.__parent is not None:
            self.__parent.__children.remove(self)

        self.__parent = other

        if self.__parent is not None:
            if sibling_index == -1 or sibling_index >= len(self.__parent.__children):
                self.__parent.__children.append(self)
            else:
                self.__parent.__children.insert(sibling_index, self)
            self.__parent.on_add_children.invoke(self)

        self.send_redraw_request()

        if self.parent:
            self.parent.send_redraw_request()

    def iterate_parents(self, func):
        if self.parent is None:
            return

        self.parent.iterate_parents(func)
        return func(self.parent)

    def get_children(self):
        return tuple(self.__children)

    def get_child(self, index):
        return self.__children[index]

    def __getitem__(self, index):
        return self.get_child(index)

    def child_count(self):
        return len(self.__children)

    def set_sibling_index(self, index):
        if self.__parent is None:
            return

        parent = self.__parent
        self.set_parent(None)
        self.set_parent(parent, index)

    def get_sibling_index(self):
        if self.__parent is None:
            return -1
        else:
            return self.__parent.__children.index(self)

    def get_rect(self):
        return pygame.Rect(*self.scaled_global_position.xy(), *self.size.xy())

    def pre_update(self, delta_time):
        for child in self.get_children():
            if child.enabled:
                child.pre_update(delta_time)

    def update(self, delta_time):
        for component in self.__components:
            if component.enabled:
                component.update(delta_time)

        for child in self.get_children():
            if child.enabled:
                child.update(delta_time)

    def event_hook(self, event):
        for component in self.__components:
            if component.enabled:
                component.event_hook(event)

        for child in self.get_children():
            if child.enabled:
                child.event_hook(event)

    def render(self, window, offset=Vector(0, 0)):
        render_pos = (self.scaled_global_position - offset)
        wnd_size = Vector(*pygame.display.get_window_size())

        # do not render objects outside window
        if render_pos.x + self.get_size().x < 0 \
                or render_pos.y + self.get_size().y < 0 \
                or render_pos.x > wnd_size.x \
                or render_pos.y > wnd_size.y:
            return

        if self.get_sprite() is not None:
            window.blit(self.get_sprite(), render_pos.xy())

        if self.draw_bounds:
            rect = pygame.Rect(*render_pos.xy(), *self.get_size().xy())
            pygame.draw.rect(window, 'red', rect)

        for child in self.get_children():
            if child.enabled:
                child.render(window, offset)

    def add_component(self, component_type: type):
        component = component_type(self)
        self.__components.append(component)
        return component

    def remove_component(self, component: Component):
        if component not in self.__components:
            raise ValueError(component)
        self.__components.remove(component)

    def get_component(self, component_type: type):
        for component in self.__components:
            if isinstance(component, component_type):
                return component
        return None

    from core.obsolete_decorator import obsolete

    @obsolete
    def set_size(self, size):
        self.size = size

    @obsolete
    def get_size(self):
        return self.size

    @obsolete
    def set_sprite(self, sprite):
        self.sprite = sprite

    @obsolete
    def get_sprite(self):
        return self.sprite

    @obsolete
    def set_parent(self, other, sibling_index=-1):
        self._set_parent_with_sibling_index(other, sibling_index)

    @obsolete
    def get_parent(self):
        return self.parent
