import sys

from core.bounds import Bounds
from core.rendering import renderer
from core import scene_manager
from core import log
from core.config import Config
from core.ui import ui_manager
from core.action import Action

import pygame

from core.vector import Vector

on_update = Action()


def close():
    log.end()
    sys.exit()


def make_window(size, fullscreen=False):
    Application.bounds().size = Vector(*size)
    flags = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.NOFRAME
    if fullscreen:
        flags |= pygame.FULLSCREEN
    return pygame.display.set_mode(size, flags)


class Application:
    _bounds = Bounds()
    _main = None

    renderers = ('direct', 'smart')

    def __init__(self, caption):
        Config.load_main()

        pygame.init()
        pygame.font.init()
        size = Config.get_value('screen_resolution').xy()
        self.target_framerate = Config.get_value('target_framerate')
        self._fullscreen = Config.get_value('screen_fullscreen', False)

        pygame.display.set_caption(caption)
        self.window = make_window(size, self.fullscreen)
        self.clock = pygame.time.Clock()

        self.rendering_type = Config.get_value('rendering_type', Application.renderers[0])
        if self.rendering_type not in Application.renderers:
            self.rendering_type = Application.renderers[0]

        self._redraw_stack = []

        Application._main = self

    def dispatch_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.VIDEORESIZE:
                self.set_resolution(Vector(*event.size))
            scene_manager.event_hook(event)

    def set_resolution(self, res):
        Config.set_value('screen_resolution', res)
        self.window = make_window(res.xy(), self.fullscreen)

    @property
    def fullscreen(self):
        return self._fullscreen

    @fullscreen.setter
    def fullscreen(self, value):
        Config.set_value('screen_fullscreen', value)
        self.window = make_window(Config.get_value('screen_resolution').xy(), value)
        self._fullscreen = value

    def run(self):
        delta_time = 0
        while True:
            self.dispatch_events()

            ui_manager.update()
            scene_manager.pre_update(delta_time)
            scene_manager.update(delta_time)

            global on_update
            on_update.invoke(delta_time)

            self.window.fill((0, 0, 0))
            renderer.render_scene(self.window)

            if self.rendering_type == 'direct':
                self.redraw_screen()

            # pygame.display.flip()
            delta_time = self.clock.tick(self.target_framerate)

            if self.rendering_type == 'smart':
                self.fill_screen()

    def redraw_request(self, rect: pygame.Rect):
        self._redraw_stack.append(rect)

    def fill_screen(self):
        requests = 0
        while self._redraw_stack:
            pygame.display.update(self._redraw_stack.pop())
            requests += 1
        # print('Screen update requests:', requests)

    def redraw_screen(self):
        pygame.display.flip()

    @staticmethod
    def get():
        return Application._main

    @staticmethod
    def bounds() -> Bounds:
        return Application._bounds
