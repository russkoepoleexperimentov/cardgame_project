import os
import pygame

DATA_PATH = 'data'

loaded_images = {}


def load_image(name):
    if name in loaded_images.keys():
        return loaded_images.get(name)

    fullname = os.path.join(DATA_PATH, name)

    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")

    image = loaded_images[name] = pygame.image.load(fullname)
    return image
