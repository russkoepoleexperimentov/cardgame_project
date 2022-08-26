import os
import pygame

from core import log
from core.obsolete_decorator import obsolete

DATA_PATH = 'data'
DEFAULT_SPRITE = 'sprites/missing_texture.jpg'


class ResourceNotLoadedException(Exception):
    pass


class Sprite:

    _game_sprites = {}
    _default_surface = pygame.image.load(os.path.join(DATA_PATH, DEFAULT_SPRITE))

    def __init__(self, path):
        self._path = path
        self._surface = None
        self._loaded = False

    @property
    def image(self):
        if not self._loaded:
            raise ResourceNotLoadedException()

        return self._surface

    def load(self):
        self._surface = pygame.image.load(self._path)

        if not self._surface:
            self._surface = Sprite._default_surface

        self._loaded = True

    def unload(self):
        self._surface = None
        self._loaded = False

    @staticmethod
    def get(path):
        if path in Sprite._game_sprites.keys():
            return Sprite._game_sprites.get(path)

        resource_path = os.path.join(DATA_PATH, path)

        sprite = Sprite(resource_path)
        sprite.load()

        Sprite._game_sprites[path] = sprite

        return sprite


@obsolete
def load_image(name):
    return Sprite.get(name).image


def load_sound(name):
    if not name:
        return None

    fullname = os.path.join(DATA_PATH, name)

    if not os.path.isfile(fullname):
        log.trace(f"sound '{fullname}' not found!")

    sound = pygame.mixer.Sound(fullname)
    return sound
