import asyncio

from core import scene_manager
from core.coroutines_manager import start_coroutine
from core.localization import translate_string
from core.resources import load_image
from core.scene import Scene
from core.ui.button import Button
from core.ui.image import Image
from core.ui.input_field import InputField
from core.ui.layout_group import HorizontalLayoutGroup
from core.vector import Vector

import pygame

from game.button_sounds import ButtonSounds
from scenes.menu import MenuScene

from game.contstants import BUTTONS_SIZE, BUTTON_DEFAULT_DESIGN


class LobbyScene(Scene):
    def __init__(self):
        super(LobbyScene, self).__init__()

        screen = Vector(*pygame.display.get_window_size())

        self.player_ready = True
        self.opponent_ready = False

        # background
        background = Image(size=screen, sprite=load_image('sprites/ui/menu_blur.png'))
        self.add_game_object(background)

        # back button
        back_btn = Button(**BUTTON_DEFAULT_DESIGN, position=Vector(40, 30), size=Vector(150, 30),
                          title=translate_string('ui.back'))
        back_btn.add_component(ButtonSounds)
        back_btn.on_click.add_listener(self.back)
        back_btn.label.set_font_size(25)
        self.add_game_object(back_btn, 150)

        # room management
        room_buttons = Image(size=Vector(screen.x, BUTTONS_SIZE.y),
                             position=Vector(40, screen.y - 100))
        l_group: HorizontalLayoutGroup = room_buttons.add_component(HorizontalLayoutGroup)
        l_group.anchor = 'left'
        l_group.spacing = 10
        room_buttons.set_parent(background)
        create_room_btn = Button(**BUTTON_DEFAULT_DESIGN, size=BUTTONS_SIZE,
                                 title=translate_string('ui.room.create'))
        create_room_btn.set_parent(room_buttons)
        join_room_btn = Button(**BUTTON_DEFAULT_DESIGN, size=BUTTONS_SIZE,
                                 title=translate_string('ui.room.join'))
        join_room_btn.set_parent(room_buttons)
        join_room_field = InputField(**BUTTON_DEFAULT_DESIGN, size=BUTTONS_SIZE,
                                     placeholder=translate_string('ui.room.join.id'))
        join_room_field.set_parent(background)
        join_room_field.position = join_room_btn.get_global_position() - Vector(0,
                                                                                BUTTONS_SIZE.y + 2)

    def load_menu(self):
        self.task.close()
        self.task = None
        scene_manager.load(MenuScene())

    def start_game(self):
        from scenes.game_scene import GameScene
        scene_manager.load(GameScene())

    def event_hook(self, event):
        super(LobbyScene, self).event_hook(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                self.opponent_ready = True

    def back(self):
        scene_manager.load(MenuScene())
