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
from game.contstants import BUTTON_DEFAULT_DESIGN, BUTTONS_SIZE
from scenes.menu import MenuScene


class StartupScene(Scene):
    def __init__(self):
        super(StartupScene, self).__init__()

        cursor.init()

        screen = Vector(*pygame.display.get_window_size())

        # background
        self.background = Image(size=screen, sprite=load_image('sprites/ui/alert_bg.png'))
        self.add_game_object(self.background)

        # connection status text
        size = Vector()
        self.connection_status_text = Text(position=Vector(screen.x // 2 - size.x // 2,
                                                           screen.y // 2 - size.y - 50),
                                           size=size, align='center', valign='middle',
                                           title='Connecting...')
        self.add_game_object(self.connection_status_text)

        layout_g = Image(position=Vector(screen.x // 2 - BUTTONS_SIZE.x // 2,
                                         screen.y - BUTTONS_SIZE.y - 300),
                         size=BUTTONS_SIZE)
        layout_g.add_component(VerticalLayoutGroup)
        self.add_game_object(layout_g)

        # username & pass fields
        self.username_field = InputField(size=BUTTONS_SIZE,
                                         sprite=BUTTON_DEFAULT_DESIGN['sprite'])
        self.username_field.set_parent(layout_g)
        self.password_field = InputField(size=BUTTONS_SIZE,
                                         sprite=BUTTON_DEFAULT_DESIGN['sprite'])
        self.password_field.set_parent(layout_g)

        # authenticate button
        self.auth_button = Button(size=BUTTONS_SIZE, title=translate_string('auth'),
                                  **BUTTON_DEFAULT_DESIGN)
        self.auth_button.on_click.add_listener(self.auth)
        self.auth_button.set_parent(layout_g)

        # register button
        self.regiseter_button = Button(size=BUTTONS_SIZE, title=translate_string('register'),
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

        application.client.on_packet.add_listener(self.on_packet)

        start_coroutine(self.wait_connection_to_server())

    async def wait_connection_to_server(self):
        while not self.connection_status:
            await asyncio.sleep(0)
        self.exit_button.enabled = True

        if self.connection_status == 'sv_success':
            self.connection_status_text.set_title('Connection success')
            await asyncio.sleep(2)
            self.connection_status_text.set_title('')

        if self.connection_status == 'sv_full':
            self.connection_status_text.set_title('Server is full')

        if self.connection_status == 'sv_connrefused':
            self.connection_status_text.set_title('Cant connect to server')

    def on_packet(self, name, *data):
        if name == 'sv_connrefused':
            self.connection_status = 'sv_connrefused'
        if name == 'sv_full':
            self.connection_status = 'sv_full'
        if name == 'sv_success':
            self.connection_status = 'sv_success'
        if name == 'register_response':
            self.connection_status_text.set_title(['register failed', 'register success'][data[0]])
        if name == 'authenticate_response':
            if data[0]:
                scene_manager.load(MenuScene())
            else:
                self.connection_status_text.set_title(data[1])

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
