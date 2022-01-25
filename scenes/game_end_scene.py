import pygame

from core import config
from core.localization import translate_string
from core.resources import load_image
from core.scene import Scene
from core.ui.image import Image
from core.ui.text import Text
from core.vector import Vector


class GameEndScene(Scene):
    def __init__(self, player_win=False):
        super(GameEndScene, self).__init__()
        self.screen_w, self.screen_h = tuple(map(int, config.get_value('vid_mode').split('x')))
        self.screen = Vector(self.screen_w, self.screen_h)

        background = Image(size=self.screen, sprite=load_image('sprites/ui/menu_blur.png'))
        self.add_game_object(background, -100)

        label, color = ('ui.win', 'green') if player_win else ('ui.loose', 'red')

        self.text = Text(size=self.screen,
                         title=translate_string(label),
                         align='center',
                         valign='middle',
                         font_size=72,
                         color=pygame.Color(color))
        self.text.set_parent(background)
