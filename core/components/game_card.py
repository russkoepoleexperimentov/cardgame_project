from core.component import Component
from core.ui.ui_element import UIElement


class GameCard(Component):
    def __init__(self, owner: UIElement):
        super(GameCard, self).__init__(owner)
