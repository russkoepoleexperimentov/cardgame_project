import sys

from core.rendering import renderer
from core import scene_manager
from core import log
from core import config
from core.ui import ui_manager

import pygame


def close():
    log.end()
    sys.exit()


class Application:
    def __init__(self, caption):
        config.load_settings()

        pygame.init()
        pygame.font.init()
        self.size = self.width, self.height = tuple(map(int, config.get_value('vid_mode').split('x')))
        self.target_framerate = int(config.get_value('target_fps'))

        pygame.display.set_caption(caption)
        self.window = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

    def dispatch_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            scene_manager.loaded_scene.event_hook(event)

    def run(self):
        delta_time = 0
        while True:
            self.dispatch_events()

            ui_manager.update()
            scene_manager.loaded_scene.update(delta_time)

            self.window.fill((0, 0, 0))
            renderer.render_scene(self.window)
            pygame.display.flip()

            delta_time = self.clock.tick(self.target_framerate)