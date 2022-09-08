import sqlite3

import pygame

from core.config import Config
from game.contstants import *
from core.resources import load_image, load_sound
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


class ChestsScene(Scene):
    def __init__(self):
        super(ChestsScene, self).__init__()
        self.card_on_screen = False
        self.card = None

        self.screen_w, self.screen_h = 1366, 768
        self.screen = Vector(self.screen_w, self.screen_h)
        background = Image(size=self.screen, sprite=load_image('sprites/ui/menu_blur.png'))
        self.add_game_object(background, -100)
        back_btn = Button(**BUTTON_DEFAULT_DESIGN, position=Vector(40, 30), size=Vector(150, 30),
                          title=translate_string('ui.back'))
        back_btn.add_component(ButtonSounds)
        back_btn.on_click.add_listener(self.back)
        back_btn.label.set_font_size(25)
        self.add_game_object(back_btn, 150)
        chest = Image(sprite=load_image('sprites/ui/chest.png'), size=Vector(500, 500),
                      position=Vector(self.screen_w // 2 - 250 + 20, 150))
        self.add_game_object(chest)
        self.chest_count = player_data_manager.get_player_data().get(PD_CHESTS)
        self.chest_info = Text(position=Vector(60, 550), size=BUTTONS_SIZE,
                          title=translate_string('ui.chest_info') + ': ' + str(self.chest_count))
        self.add_game_object(self.chest_info)
        self.open_btn = Button(**BUTTON_DEFAULT_DESIGN, position=Vector(self.screen_w // 2 - BUTTONS_SIZE.x // 2, 550),
                               size=BUTTONS_SIZE,
                          title=translate_string('ui.open'))
        self.open_btn.add_component(ButtonSounds)
        self.open_btn.on_click.add_listener(self.open_chest)
        self.add_game_object(self.open_btn)
        if self.chest_count == 0:
            self.open_btn.interactable = False

        self.card_bg = Image(size=self.screen, sprite=load_image('sprites/ui/scroll_view_back.png'))
        self.add_game_object(self.card_bg)
        self.card_bg.enabled = False

        hide_card = Button(**BUTTON_DEFAULT_DESIGN,
                           position=Vector(self.screen_w // 2 - BUTTONS_SIZE.x // 2, 604),
                           size=BUTTONS_SIZE, title='Принять')
        hide_card.set_parent(self.card_bg)
        def l(cbg=self.card_bg):
            cbg.enabled = False

        hide_card.on_click.add_listener(l)

    def open_chest(self):
        open_snd.play()
        self.chest_count -= 1

        if self.chest_count == 0:
            self.open_btn.interactable = False
        self.chest_info.set_title(translate_string('ui.chest_info') + ': ' + str(self.chest_count))

        unlock_cards = player_data_manager.get_player_data().get(PD_UNLOCKED_CARDS)
        lock_cards = list(filter(lambda x: x.section not in unlock_cards, card_manager.game_cards))

        if not lock_cards:
            return

        if not self.card_on_screen:
            '''claim_info = Text(position=Vector(750, 150), size=BUTTONS_SIZE,
                              title=translate_string('ui.congratulations') + ':')
            self.add_game_object(claim_info)'''
            self.card_on_screen = True
        else:
            self.card.set_parent(None)

        random_card_info = choice(lock_cards)
        random_card_name = random_card_info.section

        unlock_cards.append(random_card_name)
        player_data_manager.commit()

        self.card = random_card_info.build_card_object(300)
        self.card_bg.enabled = True
        self.card.position = Vector(self.screen_w // 2 - 150, 170)
        self.card.set_parent(self.card_bg)

    def event_hook(self, event):
        super().event_hook(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.back()

    def back(self):
        player_data_manager.get_player_data().update({PD_CHESTS: self.chest_count})
        player_data_manager.commit()
        card_manager.init()
        scene_manager.load(MenuScene())
