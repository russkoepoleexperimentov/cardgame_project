import asyncio

from core import scene_manager, application
from core.coroutines_manager import start_coroutine
from core.localization import translate_string
from core import log
from core.resources import load_image
from core.scene import Scene
from core.ui.button import Button
from core.ui.image import Image
from core.ui.input_field import InputField
from core.ui.layout_group import HorizontalLayoutGroup
from core.ui.text import Text
from core.vector import Vector

import pygame

from game.button_sounds import ButtonSounds
from scenes.menu import MenuScene

from game.contstants import BUTTONS_SIZE, BUTTON_DEFAULT_DESIGN


class LobbyScene(Scene):
    def __init__(self):
        super(LobbyScene, self).__init__()

        application.client.on_packet.add_listener(self.on_packet)

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
        self.buttons = room_buttons = Image(size=Vector(screen.x, BUTTONS_SIZE.y),
                             position=Vector(40, screen.y - 100))
        l_group: HorizontalLayoutGroup = room_buttons.add_component(HorizontalLayoutGroup)
        l_group.anchor = 'left'
        l_group.spacing = 10
        room_buttons.set_parent(background)
        create_room_btn = Button(**BUTTON_DEFAULT_DESIGN, size=BUTTONS_SIZE,
                                 title=translate_string('ui.room.create'))
        create_room_btn.set_parent(room_buttons)
        create_room_btn.on_click.add_listener(
            lambda: application.client.send_packet(('create_lobby',)))
        join_room_btn = Button(**BUTTON_DEFAULT_DESIGN, size=BUTTONS_SIZE,
                                 title=translate_string('ui.room.join'))
        join_room_btn.set_parent(room_buttons)
        join_room_btn.on_click.add_listener(
            lambda: application.client.send_packet(
                ('join_lobby', int(self.join_room_field.get_text()))))
        self.join_room_field = join_room_field = InputField(**BUTTON_DEFAULT_DESIGN, size=BUTTONS_SIZE,
                                     placeholder=translate_string('ui.room.join.id'))
        join_room_field.set_parent(background)
        join_room_field.position = join_room_btn.get_global_position() - Vector(0,
                                                                                BUTTONS_SIZE.y + 2)

        self.lobby_info = Text(position=Vector(40, 80), size=BUTTONS_SIZE)
        self.lobby_info.set_parent(background)
        self.leave_btn = Button(**BUTTON_DEFAULT_DESIGN, size=BUTTONS_SIZE,
                                position=Vector(40, 100), title=translate_string('ui.room.leave'))
        self.leave_btn.set_parent(background)
        self.leave_btn.on_click.add_listener(self.leave_lobby)
        self.leave_btn.enabled = False
        self.in_lobby = False

        self.l_user_me = Text(position=Vector(100, 170), size=BUTTONS_SIZE, title='Игрок 1 (вы)')
        self.l_user_me.set_parent(background)
        self.l_user_me.enabled = False
        self.l_user_other = Text(position=Vector(100, 190), size=BUTTONS_SIZE, title='Игрок 2')
        self.l_user_other.set_parent(background)
        self.l_user_other.enabled = False

        self.ready_btn = Button(**BUTTON_DEFAULT_DESIGN, size=BUTTONS_SIZE,
                                position=Vector(screen.x - 40 - BUTTONS_SIZE.x,
                                                screen.y - BUTTONS_SIZE.y - 20),
                                title=translate_string('ui.room.ready'))
        self.ready_btn.enabled = False
        self.ready_btn.on_click.add_listener(self.ready)
        self.ready_btn.set_parent(background)
        self._lobby_id = 0

    def load_menu(self):
        scene_manager.load(MenuScene())

    def start_game(self):
        from scenes.game_scene import GameScene
        scene_manager.load(GameScene())

    def event_hook(self, event):
        super(LobbyScene, self).event_hook(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                self.opponent_ready = True

    def on_packet(self, name, *data):
        if name == 'create_lobby_response':
            application.client.send_packet(('join_lobby', data[0]))

        if name == 'join_lobby_response':
            err, l_id = data
            if err:
                log.trace(err)
                return
            self.buttons.enabled = False
            self.join_room_field.enabled = False
            self.leave_btn.enabled = True
            self.lobby_info.set_title('Подключен к лобби ' + str(l_id))
            self.l_user_me.enabled = True
            self._lobby_id = l_id
            self.in_lobby = True
        if name == 'player_join':
            self.l_user_other.enabled = True
            self.ready_btn.enabled = True

        if name == 'player_left':
            self.l_user_other.enabled = False

    def leave_lobby(self):
        self.in_lobby = False
        application.client.send_packet(('leave_lobby', self._lobby_id))
        self._lobby_id = 0
        self.buttons.enabled = True
        self.join_room_field.enabled = True
        self.leave_btn.enabled = False
        self.lobby_info.set_title('')

    def back(self):
        if self.in_lobby:
            self.leave_lobby()
        scene_manager.load(MenuScene())

    def ready(self):
        application.client.send_packet(('ready', self._lobby_id))
