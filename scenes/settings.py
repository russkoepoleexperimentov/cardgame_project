import sqlite3

import pygame

from core.config import Config
from core.ui.dropdown import Dropdown
from core.ui.layout_group import VerticalLayoutGroup
from core.ui.slider import Slider
from core.ui.toggle import Toggle
from game.contstants import *
from core.resources import load_image, load_sound, Sprite
from core.scene import Scene
from core.ui.button import Button
from core.ui.image import Image
from core.ui.text import Text
from core.vector import Vector
from core.localization import translate_string
from game.button_sounds import ButtonSounds
from game.cards import card_manager
from core import scene_manager
from scenes.menu import MenuScene
from random import choice

from game import player_data_manager

open_snd = load_sound('sfx/inv_belt.ogg')
open_snd.set_volume(0.1)


class SettingsScene(Scene):
    def __init__(self):
        super(SettingsScene, self).__init__()
        self.screen_w, self.screen_h = Config.get_value('screen_resolution').xy()
        self.screen = Vector(self.screen_w, self.screen_h)

        background = Image(size=self.screen, sprite=load_image('sprites/ui/menu_blur.png'))
        self.add_game_object(background, -100)

        back_btn = Button(**BUTTON_DEFAULT_DESIGN, position=Vector(40, 30), size=Vector(150, 30),
                          title=translate_string('ui.back'))
        back_btn.add_component(ButtonSounds)
        back_btn.on_click.add_listener(self.back)
        back_btn.label.set_font_size(25)
        self.add_game_object(back_btn, 150)

        fields_bg_size = Vector(800, 600)
        fields_bg = Image(position=(self.screen - fields_bg_size) * 0.5,
                          size=fields_bg_size)
        fields_bg.parent = background
        lg: VerticalLayoutGroup = fields_bg.add_component(VerticalLayoutGroup)
        lg.spacing = 10

        self.modes = list(
            map(lambda x: f'{x[0]}x{x[1]}',
                reversed(pygame.display.list_modes())))
        self.modes.insert(0, translate_string('ui.settings.resolution.custom'))

        self.resolution_fld, ddn = self._create_settings_field(
            translate_string('ui.settings.resolution'),
            Dropdown(choices=self.modes,
                     size=BUTTONS_SIZE,
                     **BUTTON_DEFAULT_DESIGN))
        self.resolution_fld.parent = fields_bg
        ddn.on_change_value.add_listener(self.set_resolution)
        res = Config.get_value('screen_resolution', '800x600')
        res = f'{int(res.x)}x{int(res.y)}'
        try:
            ddn.select_value(res)
        except KeyError:
            ddn.select(0)

        from core.application import Application
        translated_rs = tuple(map(lambda x: translate_string('ui.settings.render.' + x), Application.renderers))
        self.render_fld, ddn = self._create_settings_field(
            translate_string('ui.settings.render'),
            Dropdown(choices=translated_rs,
                     size=BUTTONS_SIZE,
                     **BUTTON_DEFAULT_DESIGN))
        self.render_fld.parent = fields_bg
        ddn.select(self._renderer_id(Application.get().rendering_type))
        ddn.on_change_value.add_listener(self.set_renderer)

        self.fullscreen_fld, tgl = self._create_settings_field(
            translate_string('ui.settings.fullscreen'),
            Toggle(size=BUTTONS_SIZE,
                   **BUTTON_DEFAULT_DESIGN))
        self.fullscreen_fld.parent = fields_bg
        tgl.select(Application.get().fullscreen)
        tgl.on_change_value.add_listener(self.set_fullscreen)

    def _create_settings_field(self, name, field: Image, size=Vector(800, 60)):
        list_item = Image(size=size, sprite=Sprite.get('sprites/ui/scroll_view_back.png').image)
        name_label = Text(valign='middle', title=name, size=size)
        name_label.parent = list_item
        name_label.position += Vector(10, 0)
        field.parent = list_item
        field.position = Vector((list_item.size - field.size).x,
                                (list_item.size - field.size).y // 2) - Vector(10, 0)
        return list_item, field

    def _renderer_id(self, name):
        from core.application import Application
        return Application.renderers.index(name)

    def set_resolution(self, resolution_id):
        if resolution_id == 0:
            return

        resolution = self.modes[resolution_id]

        from core import config
        res = config.parse_vector(resolution)
        from core.application import Application
        Application.get().set_resolution(res)

    def set_fullscreen(self, value):
        from core.application import Application
        Application.get().fullscreen = value

    def set_renderer(self, renderer_id):
        from core.application import Application
        Application.get().rendering_type = Application.renderers[renderer_id]

    def event_hook(self, event):
        super().event_hook(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.back()

    def back(self):
        scene_manager.load(MenuScene())
