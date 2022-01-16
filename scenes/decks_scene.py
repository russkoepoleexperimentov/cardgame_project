from core import config
from core.resources import load_image
from core.scene import Scene
from core.ui.image import Image
from core.ui.text import Text
from core.vector import Vector


class DecksScene(Scene):
    def __init__(self):
        super(DecksScene, self).__init__()
        screen_w, screen_h = tuple(map(int, config.get_value('vid_mode').split('x')))
        screen = Vector(screen_w, screen_h)
        background = Image(size=screen, sprite=load_image('sprites/ui/menu.png'))
        self.add_game_object(background, -100)
        label = Text(size=Vector(screen_w, 50), title='Мои колоды', align='center', valign='middle',
                     font_size=72)
        label.set_parent(background)