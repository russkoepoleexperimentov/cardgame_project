from core.component import Component
from core.components.drag_handler import DragHandler
from core.components.drop_handler import DropHandler
from core.ui.image import Image
from core.ui.layout_group import HorizontalLayoutGroup
from game.game_scene.game_card import GameCard


class CardLine(Component):
    def __init__(self, owner: Image):
        super(CardLine, self).__init__(owner)

        # self.layout_group = owner.add_component(HorizontalLayoutGroup)
        self.allow_add_cards = True
        self.drop_handler: DropHandler = owner.add_component(DropHandler)
        self.drop_handler.on_drop.add_listener(self.on_drop)

    def add_card(self, game_card: GameCard):
        if game_card.on_table:
            return

        game_card.on_table = True
        game_card.get_game_object().set_parent(self.get_game_object())

    def on_drop(self, drag: DragHandler):
        if not self.allow_add_cards:
            return

        obj = drag.get_game_object()
        game_card: GameCard = obj.get_component(GameCard)

        if game_card:
            self.add_card(game_card)
