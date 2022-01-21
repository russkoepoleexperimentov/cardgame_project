import pygame.mouse

from core.action import Action
from core.component import Component
from core.components.drag_handler import DragHandler
from core.ui.image import Image
from core.vector import Vector
from game.cards.card import CardInfo


class GameCard(Component):
    def __init__(self, owner: Image):
        super(GameCard, self).__init__(owner)

        self.drag_offset = Vector()

        self.drag_handler: DragHandler = owner.add_component(DragHandler)
        self.drag_handler.follow_mouse = False
        self.drag_handler.on_begin_drag.add_listener(self.on_begin_drag)
        self.drag_handler.on_drag.add_listener(self.on_drag)

        self.on_die = Action()

        self._card_info = None
        self._hit_points = 0
        self._damage = 0

    def init(self, card_info: CardInfo):
        self._card_info = card_info
        self._hit_points = card_info.hit_points
        self._damage = card_info.damage

    def decrease_hit_points(self, damage: int):
        if damage < 0:
            raise ValueError()
        self._hit_points -= damage

        if self._hit_points <= 0:
            self.on_die.invoke()

    def get_hit_points(self):
        return self._hit_points

    def get_damage(self):
        return self._damage

    def get_card_info(self):
        return self._card_info

    def on_begin_drag(self):
        mouse_pos = pygame.mouse.get_pos()
        self.drag_offset = self.get_game_object().position - Vector(*mouse_pos)

    def on_drag(self):
        mouse_pos = pygame.mouse.get_pos()
        self.get_game_object().position = Vector(*mouse_pos) + self.drag_offset
