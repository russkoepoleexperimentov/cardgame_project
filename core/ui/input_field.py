
import pygame

from core.action import Action
from core.ui import ui_manager
from core.ui.image import Image
from core.ui.text import Text
from core.vector import Vector


class InputField(Image):
    def __init__(self,
                 position=Vector(),
                 size=Vector(),
                 sprite=None,
                 selected_sprite=None,
                 pressed_sprite=None,
                 disabled_sprite=None,
                 label_padding=5,
                 placeholder=''):
        super(InputField, self).__init__(position, size, sprite)
        self.interactable = True
        self.on_click = Action()
        self._text = ''
        self._active = False
        self._mouse_over = False
        self._label = Text(position=Vector(label_padding, label_padding),
                           size=size - Vector(label_padding, label_padding) * 2,
                           valign='middle', align='center')
        self._label.set_parent(self)
        self._placeholder = Text(position=Vector(label_padding, label_padding),
                                 size=size - Vector(label_padding, label_padding) * 2,
                                 valign='middle', align='center', color=pygame.Color('#A2A499'),
                                 title=placeholder)
        self._placeholder.set_parent(self)
        self._sprites = {
            'default': sprite,
            'selected': selected_sprite if selected_sprite else sprite,
            'pressed': pressed_sprite if pressed_sprite else
            selected_sprite if selected_sprite else sprite,
            'disabled': disabled_sprite if disabled_sprite else sprite
        }

    def get_text(self):
        return self._text

    def set_text(self, text):
        self._text = text
        self._label.set_title(self._text)

    def update(self, delta_time):
        super(InputField, self).update(delta_time)

        if self.interactable:
            self.set_sprite(self._sprites['default'])

            if ui_manager.get_selected() == self:
                self.set_sprite(self._sprites['selected'])

            if self._active:
                self.set_sprite(self._sprites['pressed'])
        else:
            self.set_sprite(self._sprites['disabled'])

        self._placeholder.enabled = not self._text

    def event_hook(self, event):
        super(InputField, self).event_hook(event)

        if event.type == pygame.MOUSEMOTION:
            self._mouse_over = ui_manager.get_selected() == self

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            self._active = self._mouse_over
            if self._mouse_over:
                self.on_click.invoke()

        if event.type == pygame.KEYDOWN and self._active:
            if event.key == pygame.K_BACKSPACE:
                self._text = self._text[:-1]
            elif event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_KP_ENTER):
                self._active = False
            else:
                self._text += event.unicode
            self._label.set_title(self._text)

