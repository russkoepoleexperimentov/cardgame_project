import pygame
from core.ui import ui_manager
from core.ui.image import Image
from core.ui.text import Text
from core.vector import Vector


class Button(Image):
    def __init__(self,
                 position=Vector(),
                 size=Vector(),
                 sprite=None,
                 selected_sprite=None,
                 pressed_sprite=None,
                 disabled_sprite=None,
                 title=''):
        super().__init__(position, size, sprite)

        self.sprites = {
            'default': sprite,
            'selected': selected_sprite if selected_sprite else sprite,
            'pressed': pressed_sprite if pressed_sprite else
            selected_sprite if selected_sprite else sprite,
            'disabled': disabled_sprite if disabled_sprite else sprite
        }
        self.interactable = True
        self.on_click = []
        self.mouse_over_down = False
        self.label = Text(position=self.size * 0.5, size=size, anchor='center')
        self.label.set_parent(self)
        self.set_title(title)

    def event_hook(self, event):
        super().event_hook(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if ui_manager.get_selected() == self and self.interactable:
                self.mouse_over_down = True

        if event.type == pygame.MOUSEBUTTONUP:
            if self.mouse_over_down:
                for action in self.on_click:
                    action()
            self.mouse_over_down = False
                    
    def update(self, delta_time):
        super(Button, self).update(delta_time)
        if self.interactable:
            self.sprite = self.sprites['default']

            if ui_manager.get_selected() == self:
                self.sprite = self.sprites['selected']

            if self.mouse_over_down:
                self.sprite = self.sprites['pressed']
        else:
            self.sprite = self.sprites['disabled']

    def set_title(self, title=''):
        self.label.size = self.size
        self.label.set_title(title)
