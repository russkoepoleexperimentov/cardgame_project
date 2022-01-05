import sys

from core.scene import Scene
from core.game_object import GameObject
from core.ui.button import Button
from core.ui.text import Text
from core.vector import Vector
from core.filesystem import load_image
from core.game import close_app


class MenuScene(Scene):
    def __init__(self):
        super().__init__()
        self.add_game_object(GameObject(Vector(100, 150), Vector(1024/4, 768/4), load_image('button.png')))

        button = Button(Vector(400, 150), Vector(160, 24), load_image('button.png'))
        button.on_click.append(lambda: print('agaga'))
        self.add_game_object(button)

        self.add_game_object(Text(Vector(400, 20), Vector(100, 300), title='Hearts Of Iron V'))

        exit_button = Button(
            position=Vector(0, 0),
            size=Vector(60, 60),
            sprite=load_image('exit_button.jpg'))
        exit_button.on_click.append(close_app)
        self.add_game_object(exit_button)
