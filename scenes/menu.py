import sys

from core.scene import Scene
from core.game_object import GameObject
from core.ui.button import Button
from core.ui.text import Text
from core.ui.layout_group import VerticalLayoutGroup
from core.vector import Vector
from core.filesystem import load_image
from core.game import close_app
from core import config

BUTTONS_SIZE = Vector(260, 54)
BUTTONS_TOP_OFFSET = 200


class MenuScene(Scene):
    def __init__(self):
        super().__init__()

        screen_w = int(config.get_value('vid_mode').split('x')[0])
        buttons_layout_group = VerticalLayoutGroup(Vector(screen_w // 2 - BUTTONS_SIZE.x // 2,
                                                          BUTTONS_TOP_OFFSET), 10)

        start_button = Button(
            size=BUTTONS_SIZE,
            sprite=load_image('button.png')
        )
        buttons_layout_group.add(start_button)
        self.add_game_object(start_button)

        exit_button = Button(
            size=BUTTONS_SIZE,
            sprite=load_image('button.png')
        )
        exit_button.on_click.append(close_app)
        buttons_layout_group.add(exit_button)
        self.add_game_object(exit_button)
