import os
import pygame

from core import log

DATA_PATH = 'data'

loaded_images = {}


def load_image(name):
    if not name:
        return load_image('sprites/missing_texture.jpg')

    if name in loaded_images.keys():
        return loaded_images.get(name)

    fullname = os.path.join(DATA_PATH, name)

    if not os.path.isfile(fullname):
        log.trace(f"image '{fullname}' not found!")
        return load_image('sprites/missing_texture.jpg')

    image = loaded_images[name] = pygame.image.load(fullname)
    return image


def load_sound(name):
    if not name:
        return None

    fullname = os.path.join(DATA_PATH, name)

    if not os.path.isfile(fullname):
        log.trace(f"sound '{fullname}' not found!")

    sound = pygame.mixer.Sound(fullname)
    return sound
