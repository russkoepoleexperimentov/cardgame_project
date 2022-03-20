
import pygame

from core.ui import ui_manager
from core.ui.image import Image
from core.ui.text import Text
from core.vector import Vector


class InputField(Image):
    def __init__(self, position=Vector(), size=Vector(), sprite=None, label_padding=5):
        super(InputField, self).__init__(position, size, sprite)
        self._text = ''
        self._active = False
        self._mouse_over = False
        self._label = Text(position=Vector(label_padding, label_padding),
                           size=size - Vector(label_padding, label_padding) * 2,
                           valign='middle', align='center')
        self._label.set_parent(self)

    def get_text(self):
        return self._text

    def event_hook(self, event):
        super(InputField, self).event_hook(event)

        if event.type == pygame.MOUSEMOTION:
            self._mouse_over = ui_manager.get_selected() == self

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            self._active = self._mouse_over

        if event.type == pygame.KEYDOWN and self._active:
            if event.key == pygame.K_BACKSPACE:
                self._text = self._text[:-1]
            elif event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_KP_ENTER):
                self._active = False
            else:
                self._text += event.unicode
            self._label.set_title(self._text)

