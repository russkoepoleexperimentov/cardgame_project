from core.component import Component
from core.components.drag_handler import DragHandler
from core.game_object import GameObject
from core.ui.image import Image
from core.vector import Vector
from core.resources import load_image
from core import scene_manager


class AlertPopup(Component):
    def __init__(self, owner: GameObject):
        super(AlertPopup, self).__init__(owner)
        sprite = load_image('sprites/ui/hint_wnd.png')
        self.background = Image(size=Vector(*sprite.get_size()), sprite=sprite)
        self.background.add_component(DragHandler)
        self.background.set_parent(owner)

    def hide(self):
        self.background.enabled = False

    def show(self):
        self.background.enabled = True

    def is_shown(self):
        return self.background.enabled


__popup_go = GameObject()
__instance = __popup_go.add_component(AlertPopup)
__instance.hide()
scene_manager.get_common_game_objects().add_game_object(__popup_go)


def instance():
    return __instance
