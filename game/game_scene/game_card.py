import pygame.mouse

from core.action import Action
from core.component import Component
from core.components.drag_handler import DragHandler
from core.ui.image import Image
from core.ui.layout_group import HorizontalLayoutGroup, LayoutGroup
from core.vector import Vector
from game.cards.card import CardInfo

from core import scene_manager


class GameCard(Component):
    def __init__(self, owner: Image):
        super(GameCard, self).__init__(owner)

        self.drag_offset = Vector()

        self.drag_handler: DragHandler = owner.add_component(DragHandler)
        self.drag_handler.follow_mouse = False
        self.drag_handler.on_begin_drag.add_listener(self.on_begin_drag)
        self.drag_handler.on_drag.add_listener(self.on_drag)
        self.drag_handler.on_end_drag.add_listener(self.on_end_drag)

        self.on_die = Action()

        self._card_info = None
        self._hit_points = 0
        self._damage = 0
        self.on_table = False
        self._last_parent = None
        self._last_sibling_index = -1
        self._last_position = Vector()

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
        if self.on_table:
            return

        self._last_parent = self.get_game_object().get_parent()
        self._last_sibling_index = self.get_game_object().get_sibling_index()
        self._last_position = self.get_game_object().position

        self.get_game_object().position = self.get_game_object().get_global_position()
        self.get_game_object().set_parent(None)
        mouse_pos = pygame.mouse.get_pos()
        self.drag_offset = self.get_game_object().position - Vector(*mouse_pos)

        layout_group = self._last_parent.get_component(LayoutGroup)
        if layout_group:
            layout_group.refresh()

        scene_manager.get_loaded_scene().add_game_object(self.get_game_object())

    def on_drag(self):
        if self.on_table:
            return
        mouse_pos = pygame.mouse.get_pos()
        self.get_game_object().position = Vector(*mouse_pos) + self.drag_offset

    def on_end_drag(self):
        if self.on_table:
            return

        if self.get_game_object().get_parent() is None:
            if not self.on_table:
                self.get_game_object().set_parent(self._last_parent, self._last_sibling_index)
                # self.get_game_object().position = self._last_position
                layout_group = self._last_parent.get_component(LayoutGroup)
                if layout_group:
                    layout_group.refresh()
        scene_manager.get_loaded_scene().remove_game_object(self.get_game_object())
