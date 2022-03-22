import asyncio
import os.path

import pygame

from core import application, scene_manager
from core.localization import translate_string
from core.resources import load_image
from core.scene import Scene
from core.ui.button import Button
from core.ui.image import Image
from core.ui.input_field import InputField
from core.ui.layout_group import VerticalLayoutGroup
from core.ui.text import Text
from core.vector import Vector
from core.coroutines_manager import start_coroutine
from game import cursor
from game.button_sounds import ButtonSounds
from game.cards import card_manager
from game.contstants import BUTTON_DEFAULT_DESIGN, BUTTONS_SIZE
from scenes.menu import MenuScene
from server_core.server_resources import CardInfo


class StartupScene(Scene):
    def __init__(self, username='', password=''):
        super(StartupScene, self).__init__()

        cursor.init()

        screen = Vector(*pygame.display.get_window_size())

        # background
        self.background = Image(size=screen, sprite=load_image('sprites/ui/bg_blur_1.png'))
        self.add_game_object(self.background)

        # connection status text
        size = Vector()
        self.status_text = Text(position=Vector(screen.x // 2 - size.x // 2,
                                                screen.y // 2 - size.y - 50),
                                size=size, align='center', valign='middle',
                                title=translate_string('ui.connecting'))
        self.add_game_object(self.status_text)

        layout_g = Image(position=Vector(screen.x // 2 - BUTTONS_SIZE.x // 2,
                                         screen.y - BUTTONS_SIZE.y - 300),
                         size=BUTTONS_SIZE)
        layout_g.add_component(VerticalLayoutGroup)
        self.add_game_object(layout_g)

        # username & pass fields
        self.username_field = InputField(size=BUTTONS_SIZE,
                                         **BUTTON_DEFAULT_DESIGN,
                                         placeholder=translate_string('ui.username'))
        self.username_field.set_parent(layout_g)
        self.username_field.add_component(ButtonSounds)
        self.username_field.set_text(username)
        self.password_field = InputField(size=BUTTONS_SIZE,
                                         **BUTTON_DEFAULT_DESIGN,
                                         placeholder=translate_string('ui.password'))
        self.password_field.set_parent(layout_g)
        self.password_field.add_component(ButtonSounds)
        self.password_field.set_text(password)

        # authenticate button
        self.auth_button = Button(size=BUTTONS_SIZE, title=translate_string('ui.login'),
                                  **BUTTON_DEFAULT_DESIGN)
        self.auth_button.on_click.add_listener(self.auth)
        self.auth_button.set_parent(layout_g)

        # register button
        self.regiseter_button = Button(size=BUTTONS_SIZE, title=translate_string('ui.register'),
                                       **BUTTON_DEFAULT_DESIGN)
        self.regiseter_button.on_click.add_listener(self.register)
        self.regiseter_button.set_parent(layout_g)

        # exit button
        self.exit_button = Button(size=BUTTONS_SIZE, title=translate_string('ui.quit'),
                                  **BUTTON_DEFAULT_DESIGN)
        self.exit_button.add_component(ButtonSounds)
        self.exit_button.enabled = False
        self.exit_button.on_click.add_listener(application.close)
        self.exit_button.set_parent(layout_g)

        self.connection_status = ''

        self.resources_count = 0
        self.resources_loaded = False
        self.resource_downloading = ''

        self.username_field.enabled = False
        self.password_field.enabled = False
        self.auth_button.enabled = False
        self.regiseter_button.enabled = False

        application.client.on_packet.add_listener(self.on_packet)

        start_coroutine(self.wait_connection_to_server())

    async def wait_connection_to_server(self):
        while not self.connection_status:
            await asyncio.sleep(0)
        self.exit_button.enabled = True

        if self.connection_status == 'sv_success':
            self.show_hint(translate_string('ui.connection_success'), 4)
            self.username_field.enabled = True
            self.password_field.enabled = True
            self.auth_button.enabled = True
            self.regiseter_button.enabled = True

            # if we received auth data from main.py
            if self.username_field.get_text() and self.password_field.get_text():
                self.auth(self.username_field.get_text(), self.password_field.get_text())

        if self.connection_status == 'sv_full':
            self.status_text.set_title(translate_string('ui.server_full'))

        if self.connection_status == 'sv_connrefused':
            self.status_text.set_title(translate_string('ui.connection_failed'))

    def on_packet(self, name, *data):
        if name == 'sv_connrefused':
            self.connection_status = 'sv_connrefused'
        if name == 'sv_full':
            self.connection_status = 'sv_full'
        if name == 'sv_success':
            self.connection_status = 'sv_success'
        if name == 'register_response':
            self.show_hint(translate_string(['ui.reg_failed', 'ui.reg_success'][data[0]]), 5)
        if name == 'authenticate_response':
            if data[0]:
                application.client.send_packet(('get_all_cards',))
            else:
                self.show_hint(translate_string('ui.auth_failed') + ': ' + data[1])
        if name == 'all_cards_response':
            cards = tuple(map(lambda x: CardInfo(*x), data[0]))
            card_manager.register_cards(cards)
            scene_manager.load(MenuScene())

    def update(self, delta_time):
        super(StartupScene, self).update(delta_time)
        self.regiseter_button.interactable = self.auth_button.interactable = \
            self.username_field.get_text() and self.password_field.get_text()

    def register(self):
        username, password = self.username_field.get_text(), self.password_field.get_text()
        application.client.register(username, password)

    def auth(self, username='', password=''):
        if not username:
            username, password = self.username_field.get_text(), self.password_field.get_text()
        application.client.authenticate(username, password)

    def show_hint(self, hint: str, delay=4):
        start_coroutine(self._show_hint_routine(hint, delay))

    async def _show_hint_routine(self, hint, delay):
        self.status_text.set_title(hint)
        await asyncio.sleep(delay)
        self.status_text.set_title('')

