import sys

from core.scene import Scene
from core.game_object import GameObject
from core.ui.button import Button
from core.vector import Vector
from core.filesystem import load_image


class MenuScene(Scene):
    def __init__(self):
        super().__init__()
        self.add_game_object(GameObject(Vector(100, 150), Vector(1024/4, 768/4), load_image('button.png')))

        button = Button(Vector(400, 150), Vector(160, 24), load_image('button.png'))
        button.on_click.append(lambda: print('agaga'))
        self.add_game_object(button)

        exit_button = Button(
            position=Vector(0, 0),
            size=Vector(60, 60),
            sprite=load_image('exit_button.jpg'))
        exit_button.on_click.append(sys.exit)
        self.add_game_object(exit_button)
