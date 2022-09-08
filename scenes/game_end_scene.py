import random

import pygame

from core import config, scene_manager
from core.localization import translate_string
from core.resources import load_image
from core.scene import Scene
from core.ui.button import Button
from core.ui.image import Image
from core.ui.text import Text
from core.vector import Vector
from game import player_data_manager
from game.contstants import *

WIN_CHESTS_MIN, WIN_CHESTS_MAX = 2, 4

GAME_RESULT_LABEL_SIZE = Vector(384, 105)
GAME_RESULT_LABEL_OFFSET = Vector(0, -150)
FONT_SIZE = 64


class GameEndScene(Scene):
    def __init__(self, player_win=False):
        super(GameEndScene, self).__init__()
        self.screen_w, self.screen_h = 1366, 768
        self.screen = Vector(self.screen_w, self.screen_h)

        background = Image(size=self.screen, sprite=load_image('sprites/ui/menu_blur.png'))
        self.add_game_object(background, -100)

        result_bg = Image(size=GAME_RESULT_LABEL_SIZE,
                          position=Vector(self.screen_w // 2 - GAME_RESULT_LABEL_SIZE.x // 2,
                                          self.screen_h // 2 - GAME_RESULT_LABEL_SIZE.y // 2) +
                                   GAME_RESULT_LABEL_OFFSET,
                          sprite=load_image('sprites/ui/hint_wnd.png'))
        result_bg.set_parent(background)

        label, color = ('ui.win', '#186A3B') if player_win else ('ui.loose', '#A93226')

        self.text = Text(size=GAME_RESULT_LABEL_SIZE,
                         title=translate_string(label),
                         align='center',
                         valign='middle',
                         font_size=FONT_SIZE,
                         color=pygame.Color(color))
        self.text.set_parent(result_bg)

        if player_win:
            added_chests = random.randint(WIN_CHESTS_MIN, WIN_CHESTS_MAX)

            chest_label = Text(size=result_bg.get_size(),
                               position=result_bg.position - GAME_RESULT_LABEL_OFFSET,
                               title=translate_string('ui.chests_added').format(added_chests),
                               align='center',
                               color=pygame.Color('#5D6D7E'))
            chest_label.set_parent(background)

            player_data_manager.get_player_data()[PD_CHESTS] += added_chests
            player_data_manager.commit()

        to_menu_btn = Button(**BUTTON_DEFAULT_DESIGN,
                             size=BUTTONS_SIZE,
                             position=Vector(self.screen_w // 2 - BUTTONS_SIZE.x // 2,
                                             self.screen_h // 2 + GAME_RESULT_LABEL_SIZE.y),
                             title=translate_string('ui.continue'))
        to_menu_btn.set_parent(background)
        to_menu_btn.on_click.add_listener(self.load_menu)

    def event_hook(self, event):
        super().event_hook(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.load_menu()

    def load_menu(self):
        from scenes.menu import MenuScene
        scene_manager.load(MenuScene())
