import asyncio

from core import scene_manager
from core.coroutines_manager import start_coroutine
from core.localization import translate_string
from core.resources import load_image
from core.scene import Scene
from core.ui.button import Button
from core.ui.image import Image
from core.vector import Vector

import pygame

from game.button_sounds import ButtonSounds
from scenes.menu import MenuScene

from game.contstants import BUTTONS_SIZE, BUTTON_DEFAULT_DESIGN


class LobbyScene(Scene):
    def __init__(self):
        super(LobbyScene, self).__init__()

        screen = Vector(*pygame.display.get_window_size())

        # task
        self.task = self.wait_for_play()
        start_coroutine(self.task)

        self.player_ready = True
        self.opponent_ready = False

        # background
        background = Image(size=screen, sprite=load_image('sprites/ui/menu_blur.png'))
        self.add_game_object(background)

        # back button
        back_btn = Button(position=Vector(10, screen.y - BUTTONS_SIZE.y - 10), size=BUTTONS_SIZE,
                          **BUTTON_DEFAULT_DESIGN, title=translate_string('ui.back'))
        back_btn.on_click.add_listener(self.load_menu)
        back_btn.add_component(ButtonSounds)
        back_btn.set_parent(background)

        #

    def load_menu(self):
        self.task.close()
        self.task = None
        scene_manager.load(MenuScene())

    async def wait_for_play(self):
        while not (self.player_ready and self.opponent_ready):
            try:
                await asyncio.sleep(0)
            except asyncio.CancelledError:
                return
        self.start_game()

    def start_game(self):
        from scenes.game_scene import GameScene
        scene_manager.load(GameScene())

    def event_hook(self, event):
        super(LobbyScene, self).event_hook(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                self.opponent_ready = True
