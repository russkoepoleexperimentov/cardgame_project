from core.action import Action
from core.ui.ui_element import UIElement
from core.components.drag_handler import DragHandler
from core import scene_manager

on_ui_update = Action()
__selected = None
__dragged = None


def get_selected():
    return __selected


def set_selected(other: UIElement):
    global __selected
    __selected = other


def get_dragged():
    return __dragged


def set_dragged(other: DragHandler):
    global __dragged
    __dragged = other


def remove_dragged():
    global __dragged
    __dragged = None


def update():
    global __selected
    __selected = None
    for game_object in scene_manager.loaded_scene.get_game_objects():
        if isinstance(game_object, UIElement):
            game_object.update_ui_selected()
