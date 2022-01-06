from core.ui.ui_element import UIElement

__selected = None


def get_selected():
    return __selected


def set_selected(other: UIElement):
    global __selected
    __selected = other


def update():
    global __selected
    __selected = None
