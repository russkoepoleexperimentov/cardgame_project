from core import scene_manager
from core.component import Component
from core.components.drag_handler import DragHandler
from core.game_object import GameObject
from core.localization import translate_string
from core.resources import load_image
from core.ui.button import Button
from core.ui.image import Image
from core.ui.text import Text
from core.vector import Vector
from core import config

import asyncio

from game.contstants import BUTTON_DEFAULT_DESIGN
from game.button_sounds import ButtonSounds

BUTTONS_SIZE = Vector(86, 28)
BORDER_OFFSET = 10
BUTTONS_MARGIN = 2


class AlertPopup(Component):
    def __init__(self, owner: GameObject):
        super(AlertPopup, self).__init__(owner)
        sprite = load_image('sprites/ui/hint_wnd.png')
        sprite_size = Vector(*sprite.get_size())

        screen = Vector(*map(int, config.get_value('vid_mode').split('x')))

        self.input_disabler = Image(position=Vector(), size=screen)
        self.input_disabler.set_parent(owner)
        self.input_disabler.enabled = False

        self.background = Image(position=Vector((screen.x - sprite_size.x) / 2,
                                                (screen.y - sprite_size.y) / 2),
                                size=sprite_size,
                                sprite=sprite)
        self.background.set_parent(self.input_disabler)

        btn_y = sprite_size.y - BORDER_OFFSET - BUTTONS_SIZE.y

        self.yes_btn = Button(**BUTTON_DEFAULT_DESIGN,
                              size=BUTTONS_SIZE,
                              title=translate_string('ui.yes'),
                              position=Vector(sprite_size.x - BUTTONS_SIZE.x * 2 - BORDER_OFFSET - BUTTONS_MARGIN,
                                              btn_y))
        self.yes_btn.add_component(ButtonSounds)
        self.yes_btn.on_click.add_listener(self.on_accepted)
        self.yes_btn.set_parent(self.background)

        self.no_btn = Button(**BUTTON_DEFAULT_DESIGN,
                             size=BUTTONS_SIZE,
                             title=translate_string('ui.no'),
                             position=Vector(sprite_size.x - BUTTONS_SIZE.x - BORDER_OFFSET,
                                             btn_y))
        self.no_btn.add_component(ButtonSounds)
        self.no_btn.on_click.add_listener(self.on_canceled)
        self.no_btn.set_parent(self.background)

        self.title = Text(position=Vector(BORDER_OFFSET, BORDER_OFFSET),
                          size=sprite_size-Vector(BORDER_OFFSET, BORDER_OFFSET) * 2,
                          title='')

        self.__result = asyncio.Future()

    async def await_for_decision(self, text: str):
        self.input_disabler.enabled = True
        self.title.set_title(text)
        self.__result = asyncio.Future()
        # result = await self.__result
        await asyncio.sleep(2)
        print('afafafsaf')
        self.input_disabler.enabled = False
        return True

    def on_accepted(self):
        self.__result.set_result(True)

    def on_canceled(self):
        self.__result.set_result(False)


__instance = None


def init():
    global __instance
    __popup_go = GameObject()
    __instance = __popup_go.add_component(AlertPopup)
    scene_manager.get_common_game_objects().add_game_object(__popup_go, priority=100)


def instance() -> AlertPopup:
    return __instance
