import asyncio

import pygame

from core import application, scene_manager
from core.localization import translate_string
from core.resources import load_image
from core.scene import Scene
from core.ui.button import Button
from core.ui.image import Image
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
                                                           screen.y // 2 - size.y),
                                           size=size, align='center', valign='middle',
                                           title='Connecting...')
        self.add_game_object(self.connection_status_text)

        # exit button
        self.exit_button = Button(position=Vector(screen.x // 2 - BUTTONS_SIZE.x // 2,
                                                  screen.y - BUTTONS_SIZE.y - 100),
                                  size=BUTTONS_SIZE, title=translate_string('ui.quit'),
                                  **BUTTON_DEFAULT_DESIGN)
        self.exit_button.add_component(ButtonSounds)
        self.exit_button.enabled = False
        self.exit_button.on_click.add_listener(application.close)
        self.add_game_object(self.exit_button)

        self.connection_status = ''

        application.client.on_packet.add_listener(self.on_packet)

        start_coroutine(self.wait_connection_to_server())

    async def wait_connection_to_server(self):
        while not self.connection_status:
            await asyncio.sleep(0)

        if self.connection_status == 'sv_success':
            self.connection_status_text.set_title('Connection success')
            await asyncio.sleep(0.5)
            self.connection_status_text.set_title('Continue play')
            await asyncio.sleep(1)

            scene_manager.load(MenuScene())

        if self.connection_status == 'sv_full':
            self.connection_status_text.set_title('Server is full')
            self.exit_button.enabled = True

        if self.connection_status == 'sv_connrefused':
            self.connection_status_text.set_title('Cant connect to server')
            self.exit_button.enabled = True


    def on_packet(self, name, *data):
        if name == 'sv_connrefused':
            self.connection_status = 'sv_connrefused'
        if name == 'sv_full':
            self.connection_status = 'sv_full'
        if name == 'sv_success':
            self.connection_status = 'sv_success'
