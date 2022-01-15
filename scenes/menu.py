from core.scene import Scene
from core.ui.image import Image
from core.ui.button import Button
from core.ui.text import Text
from core.ui.layout_group import VerticalLayoutGroup
from core.vector import Vector
from core.resources import load_image
from core.application import close as close_app
from core.components.drag_handler import DragHandler
from core.components.drop_handler import DropHandler
from core.localization import translate_string
from core import config

from game import cursor
from game.button_sounds import ButtonSounds
from game.contstants import BUTTON_DEFAULT_DESIGN, BUTTONS_SIZE, BUTTONS_TOP_OFFSET
from game import alert_popup


import asyncio
import threading


async def wait_des():
    await alert_popup.instance().await_for_decision('agasgas')


def do_smth():
    threading.Thread(target=asyncio.run(wait_des())).start()


class MenuScene(Scene):
    def __init__(self):
        super().__init__()

        cursor.init()
        alert_popup.init()

        screen_w, screen_h = tuple(map(int, config.get_value('vid_mode').split('x')))
        screen = Vector(screen_w, screen_h)
        buttons_layout_group = VerticalLayoutGroup(position=Vector(screen_w // 2 - BUTTONS_SIZE.x // 2,
                                                                   BUTTONS_TOP_OFFSET), spacing=10)
        buttons_layout_group.draw_bounds = True
        self.add_game_object(buttons_layout_group)

        background = Image(size=screen, sprite=load_image('sprites/ui/menu.png'))
        self.add_game_object(background, -100)

        game_title = Text(size=BUTTONS_SIZE, title=translate_string('game_name'), align='center', valign='middle')
        game_title.set_parent(buttons_layout_group)

        start_button = Button(**BUTTON_DEFAULT_DESIGN, size=BUTTONS_SIZE, title=translate_string('ui.start'))
        start_button.set_parent(buttons_layout_group)
        start_button.add_component(ButtonSounds)
        start_button.on_click.add_listener(do_smth)

        settings_button = Button(**BUTTON_DEFAULT_DESIGN, size=BUTTONS_SIZE, title=translate_string('ui.settings'))
        settings_button.set_parent(buttons_layout_group)
        settings_button.add_component(ButtonSounds)
        settings_button.interactable = False

        exit_button = Button(**BUTTON_DEFAULT_DESIGN, size=BUTTONS_SIZE, title=translate_string('ui.quit'))
        exit_button.set_parent(buttons_layout_group)
        exit_button.add_component(ButtonSounds)
        exit_button.on_click.add_listener(close_app)

        # drop_handle = exit_button.add_component(DropHandler)
        # drop_handle.on_drop.add_listener(lambda drag: print(drag))

        # test_drag_go = Image(size=Vector(100, 100),
        # position=Vector(50, 50), sprite=load_image('sprites/ui/button.png'))
        # test_drag_go.add_component(DragHandler)
        # self.add_game_object(test_drag_go)
