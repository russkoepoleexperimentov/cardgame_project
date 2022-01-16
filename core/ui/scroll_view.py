import pygame

from core.ui import ui_manager
from core.ui.image import Image
from core.ui.slider import Slider, MOUSE_WHEEL_SENSETIVITY
from core.vector import Vector


class ScrollView(Image):
    def __init__(self,
                 position=Vector(),
                 size=Vector(),
                 background_sprite=None,
                 slider_width=40,
                 slider_background_sprite=None,
                 slider_handle_sprite=None,
                 content_type=Image):
        super(ScrollView, self).__init__(position, size, background_sprite)
        self.slider = Slider(position=size.xo(), size=Vector(slider_width, size.y),
                             background_sprite=slider_background_sprite,
                             handle_sprite=slider_handle_sprite)
        self.slider.set_scale(slider_width)
        self.slider.on_value_changed.add_listener(self.move_content)
        self.slider.set_parent(self)
        self.min_slider_width = slider_width

        self.content = content_type(size=size + Vector(0, size.y * 3))
        self.content.set_parent(self)
        self.content.render = self.render_content

        self.content_offset = Vector()

        self.rescale_slider()

    def move_content(self, value):
        self.content.position = self.content_offset + Vector(0, -value *
                                       (self.content.get_size().y - self.get_size().y))

    def render_content(self, window, offset=Vector(0, 0)):
        surface = pygame.surface.Surface(size=(self.get_size().xy()), flags=pygame.SRCALPHA)

        for child in self.content.get_children():
            if child.enabled:
                child.render(surface, self.get_global_position())

        window.blit(surface, self.get_global_position().xy())

    def rescale_slider(self):
        scale = self.content.get_size().y / self.get_size().y
        self.slider.set_scale(max(self.min_slider_width, self.slider.get_size().y / scale))

    def event_hook(self, event):
        super().event_hook(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if ui_manager.get_selected() in (self, self.content):
                if event.button == 4:
                    self.slider.set_value(self.slider.get_value() - MOUSE_WHEEL_SENSETIVITY)
                elif event.button == 5:
                    self.slider.set_value(self.slider.get_value() + MOUSE_WHEEL_SENSETIVITY)