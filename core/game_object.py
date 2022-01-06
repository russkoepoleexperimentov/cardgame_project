import pygame
from core.vector import Vector


class GameObject:
    def __init__(self, position=Vector(), size=Vector(), sprite=None):
        self.position = position
        self.size = size
        self.sprite = sprite
        self.draw_bounds = False
        self.on_update = []

        self.__parent = None
        self.__children = []

    def set_parent(self, other):
        if self.__parent is not None:
            self.__parent.__children.remove(other)

        self.__parent = other

        if other is not None:
            other.__children.append(self)
            other.on_add_children(self)

    def get_parent(self):
        return self.__parent

    def get_children(self):
        return tuple(self.__children)

    def __getitem__(self, index):
        return self.__children[index]

    def get_sibling_index(self):
        if self.__parent is None:
            return -1
        else:
            return self.__parent.__children.index(self)

    def on_add_children(self, other):
        pass

    def get_global_position(self):
        if self.__parent is None:
            return self.position
        else:
            return self.__parent.get_global_position() + self.position

    def get_rect(self):
        return pygame.Rect(*self.get_global_position().xy(), *self.size.xy())

    def update(self):
        for method in self.on_update:
            method()

    def event_hook(self, event):
        pass

    def render(self, window):
        if self.sprite is not None:
            sprite = pygame.transform.scale(self.sprite, self.size.xy())
            window.blit(sprite, self.get_global_position().xy())

        if self.draw_bounds:
            pygame.draw.rect(window, 'red', self.get_rect())

        for child in self.get_children():
            child.render(window)
