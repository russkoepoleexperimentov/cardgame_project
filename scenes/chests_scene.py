import sqlite3

import pygame

from core import config, application
from game.contstants import *
from core.resources import load_image
from core.scene import Scene
from core.ui.button import Button
from core.ui.image import Image
from core.ui.text import Text
from core.vector import Vector
from core.localization import translate_string
from game.button_sounds import ButtonSounds
from game.cards import card_manager, card_object_manager
from core import scene_manager
from scenes.menu import MenuScene
from random import choice

from game import player_data_manager


class ChestsScene(Scene):
    def __init__(self):
        super(ChestsScene, self).__init__()
        self.card_on_screen = False
        self.card = None

        self.screen_w, self.screen_h = tuple(map(int, config.get_value('vid_mode').split('x')))
        self.screen = Vector(self.screen_w, self.screen_h)
        self.bg = background = Image(size=self.screen, sprite=load_image('sprites/ui/menu_blur.png'))
        self.add_game_object(background, -100)
        back_btn = Button(**BUTTON_DEFAULT_DESIGN, position=Vector(40, 30), size=Vector(150, 30),
                          title=translate_string('ui.back'))
        back_btn.add_component(ButtonSounds)
        back_btn.on_click.add_listener(self.back)
        back_btn.label.set_font_size(25)
        self.add_game_object(back_btn, 150)
        chest = Image(sprite=load_image('sprites/ui/chest.png'), size=Vector(350, 350),
                      position=Vector(50, 150))
        self.add_game_object(chest)

        application.client.on_packet.add_listener(self.on_packet)
        self.chest_count = 0

        self.chest_info = Text(position=Vector(60, 550), size=BUTTONS_SIZE,
                          title=translate_string('ui.chest_info') + ': ' + str(self.chest_count))
        self.add_game_object(self.chest_info)
        self.open_btn = Button(**BUTTON_DEFAULT_DESIGN, position=Vector(60, 580), size=BUTTONS_SIZE,
                          title=translate_string('ui.open'))
        self.open_btn.add_component(ButtonSounds)
        self.open_btn.on_click.add_listener(self.open_chest)
        self.add_game_object(self.open_btn)
        #self.open_btn.interactable = False

        self._card = None

        application.client.send_packet(('get_chests_count',))

    def open_chest(self):
        self.chest_count -= 1
        self.open_btn.interactable = self.chest_count > 0
        self.chest_info.set_title(translate_string('ui.chest_info') + ': ' +
                                  str(self.chest_count))
        application.client.send_packet(('open_chest',))

    def event_hook(self, event):
        super().event_hook(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.back()

    def back(self):
        application.client.on_packet.remove_listener(self.on_packet)
        scene_manager.load(MenuScene())

    def on_packet(self, name, *data):
        if name == 'chests_count_response':
            self.chest_count = data[0]
            self.open_btn.interactable = self.chest_count > 0
            self.chest_info.set_title(translate_string('ui.chest_info') + ': ' +
                                      str(self.chest_count))
        if name == 'open_chest_response':
            if not data[0]:
                return
            section = data[0]
            card = card_manager.game_cards[section]
            card_manager.unlocked_cards_by_nation[card.nation].append(section)

            if self._card:
                self._card.set_parent(None)
                self._card = None

            self._card = card_object_manager.build_card_object(card)
            self._card.position = Vector(800, 50)
            self._card.set_parent(self.bg)
