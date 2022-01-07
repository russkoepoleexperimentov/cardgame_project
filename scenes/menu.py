from core.scene import Scene
from core.ui.image import Image
from core.ui.button import Button
from core.ui.layout_group import VerticalLayoutGroup
from core.vector import Vector
from core.resources import load_image
from core.application import close
from core.components.drag_handler import DragHandler
from core import config

BUTTONS_SIZE = Vector(260, 54)
BUTTONS_TOP_OFFSET = 200

button_design = {
    'size': BUTTONS_SIZE,
    'sprite': load_image('button.png'),
    'pressed_sprite': load_image('button_p.png'),
    'selected_sprite': load_image('button_s.png'),
    'disabled_sprite': load_image('button_d.png'),
}


class MenuScene(Scene):
    def __init__(self):
        super().__init__()

        screen_w = int(config.get_value('vid_mode').split('x')[0])
        buttons_layout_group = VerticalLayoutGroup(position=Vector(screen_w // 2 - BUTTONS_SIZE.x // 2,
                                                                   BUTTONS_TOP_OFFSET), spacing=10)
        buttons_layout_group.draw_bounds = True
        self.add_game_object(buttons_layout_group)

        start_button = Button(**button_design, title='Start')
        start_button.set_parent(buttons_layout_group)
        self.add_game_object(start_button)

        exit_button = Button(**button_design, title='Exit')
        exit_button.on_click.add_listener(close)
        exit_button.set_parent(buttons_layout_group)
        self.add_game_object(exit_button)

        test_drag_go = Image(size=Vector(100, 100), position=Vector(50, 50), sprite=load_image('button.png'))
        drag_handler = test_drag_go.add_component(DragHandler)
        self.add_game_object(test_drag_go)
