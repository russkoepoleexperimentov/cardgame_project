import sys

from render import renderer
from core import scene_manager

import settings
import pygame


class Game:
    def __init__(self, caption):
        global window_global
        self.size = self.width, self.height = settings.WND_SIZE
        self.target_framerate = settings.TARGET_FRAMERATE

        pygame.display.set_caption(caption)
        self.window = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

    def dispatch_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def run(self):
        pygame.init()
        while True:
            self.dispatch_events()

            scene_manager.loaded_scene.update_objects()

            self.window.fill((0, 0, 0))
            renderer.render_scene(self.window)
            pygame.display.flip()

            self.clock.tick(self.target_framerate)
