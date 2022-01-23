import pygame

from core.component import Component
from core.components.drag_handler import DragHandler
from core.components.drop_handler import DropHandler
from core.ui import ui_manager
from core.ui.image import Image
from core.ui.layout_group import HorizontalLayoutGroup, LayoutGroup
from game.game_scene.game_card import GameCard, get_temp_card, get_temp_card_parent

TYPE_PLAYER = 'player_line'
TYPE_ENEMY = 'enemy_line'
TYPES_LINE = (TYPE_PLAYER, TYPE_ENEMY)
TYPE_PLAYER_HAND = 'player_hand'
TYPE_ENEMY_HAND = 'enemy_hand'
TYPES_HAND = (TYPE_ENEMY_HAND, TYPE_PLAYER_HAND)


class CardLine(Component):
    def __init__(self, owner: Image):
        super(CardLine, self).__init__(owner)

        # self.layout_group = owner.add_component(HorizontalLayoutGroup)
        self.type = '-1'
        self.drop_handler: DropHandler = owner.add_component(DropHandler)
        self.drop_handler.on_drop.add_listener(self.on_drop)

        self.mouse_inside = False

    def add_card(self, game_card: GameCard):
        if game_card.on_table:
            return

        if self.type in TYPES_LINE:
            game_card.on_table = True
        game_card.get_game_object().set_parent(self.get_game_object())

    def on_drop(self, drag: DragHandler):
        if not self.type == TYPE_PLAYER:
            return

        obj = drag.get_game_object()
        game_card: GameCard = obj.get_component(GameCard)

        if game_card:
            self.add_card(game_card)

    def event_hook(self, event):
        if not self.type == TYPE_PLAYER or \
                ui_manager.get_dragged() is None or \
                get_temp_card() is None:
            return

        dragged = ui_manager.get_dragged().get_game_object()
        if event.type == pygame.MOUSEMOTION:
            bounds: pygame.Rect = self.get_game_object().get_rect()
            mouse_pos = pygame.mouse.get_pos()

            if bounds.collidepoint(mouse_pos) and not self.mouse_inside:
                self.mouse_inside = True

                # on pointer enter
                game_card: GameCard = dragged.get_component(GameCard)
                if game_card and not game_card.on_table:
                    get_temp_card().set_parent(self.get_game_object())

            if not bounds.collidepoint(mouse_pos) and self.mouse_inside:
                self.mouse_inside = False

                # on pointer exit
                game_card: GameCard = dragged.get_component(GameCard)
                if game_card and get_temp_card().get_parent() == self.get_game_object():
                    get_temp_card().set_parent(get_temp_card_parent())
                    layout_group = self.get_game_object().get_component(LayoutGroup)
                    if layout_group:
                        layout_group.refresh()
