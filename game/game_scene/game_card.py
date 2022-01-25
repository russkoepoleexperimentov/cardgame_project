import pygame.mouse

from core.action import Action
from core.component import Component
from core.components.drag_handler import DragHandler
from core.components.drop_handler import DropHandler
from core.resources import load_image, load_sound
from core.ui import ui_manager
from core.ui.image import Image
from core.ui.layout_group import HorizontalLayoutGroup, LayoutGroup
from core.vector import Vector
from game.cards.card import CardInfo, hp_text_index, highlight_index

from core import scene_manager
from game.game_scene import game_manager

temp_card_parent: Image = None
temp_card: Image = None
error_sound = load_sound('sfx/error.wav')
card_drag_start = load_sound('sfx/action_open.wav')
card_drag_end = load_sound('sfx/action_close.wav')
fight_sound = load_sound('sfx/cards_fight.wav')


def get_temp_card():
    return temp_card


def get_temp_card_parent():
    return temp_card_parent


def init_temp_card(size=Vector()):
    global temp_card
    if temp_card is not None:
        return

    temp_card = Image(size=size, sprite=load_image('sprites/card_shadow.png'))
    temp_card.block_raycasts = False
    # scene_manager.get_loaded_scene().add_game_object(temp_card, 110)


class GameCard(Component):
    def __init__(self, owner: Image):
        super(GameCard, self).__init__(owner)

        self.drag_offset = Vector()

        self.drag_handler: DragHandler = owner.add_component(DragHandler)
        self.drag_handler.follow_mouse = False
        self.drag_handler.on_begin_drag.add_listener(self.on_begin_drag)
        self.drag_handler.on_drag.add_listener(self.on_drag)
        self.drag_handler.on_end_drag.add_listener(self.on_end_drag)

        self.drop_handler: DropHandler = owner.add_component(DropHandler)
        self.drop_handler.on_drop.add_listener(self.on_drop)

        self.on_die = Action()

        self._card_info = None
        self._hit_points = 0
        self._damage = 0
        self.on_table = False
        self.can_attack = False
        self.attack_used = False
        self._last_parent = None
        self._last_sibling_index = -1
        self.owned_by_player = False

        init_temp_card(owner.get_size())

    def init(self, card_info: CardInfo, is_player=False):
        self._card_info = card_info
        self._hit_points = card_info.hit_points
        self._damage = card_info.damage
        self.owned_by_player = is_player

    def decrease_hit_points(self, damage: int):
        if damage < 0:
            raise ValueError()
        self._hit_points -= damage

        text = self.get_game_object().get_child(hp_text_index())

        if self._hit_points <= 0:
            self.on_die.invoke()
            text.set_title('0')

            # destroy
            self.get_game_object().set_parent(None)
        else:
            text.set_title(str(self._hit_points))

    def get_hit_points(self):
        return self._hit_points

    def get_damage(self):
        return self._damage

    def get_card_info(self):
        return self._card_info

    def on_begin_drag(self):
        global temp_card_parent

        if not game_manager.is_player_turn() or not game_manager.is_player_card(self):
            self.get_game_object().block_raycasts = True
            ui_manager.remove_dragged()
            return

        self._last_parent = temp_card_parent = self.get_game_object().get_parent()
        self._last_sibling_index = self.get_game_object().get_sibling_index()

        self.get_game_object().position = self.get_game_object().get_global_position()
        self.get_game_object().set_parent(None)
        mouse_pos = pygame.mouse.get_pos()
        self.drag_offset = self.get_game_object().position - Vector(*mouse_pos)

        temp_card.set_parent(temp_card_parent)
        temp_card.set_sibling_index(self._last_sibling_index)

        scene_manager.get_loaded_scene().add_game_object(self.get_game_object())
        card_drag_start.play()

    def on_drag(self):

        mouse_pos = pygame.mouse.get_pos()
        self.get_game_object().position = Vector(*mouse_pos) + self.drag_offset

        self.check_position()

    def on_end_drag(self):
        if self.get_game_object().get_parent() is None:
            self.get_game_object().set_parent(self._last_parent, self._last_sibling_index)

        self.get_game_object().set_sibling_index(temp_card.get_sibling_index())
        temp_card.set_parent(None)

        layout_group = self._last_parent.get_component(LayoutGroup)
        if layout_group:
            layout_group.refresh()

        layout_group = self.get_game_object().get_parent().get_component(LayoutGroup)
        if layout_group:
            layout_group.refresh()

        scene_manager.get_loaded_scene().remove_game_object(self.get_game_object())

        if self._hit_points <= 0:
            # destroy
            self.get_game_object().set_parent(None)

        card_drag_end.play()
        game_manager.refresh_card_parents()

    def on_drop(self, drag: DragHandler):
        obj = drag.get_game_object()
        game_card: GameCard = obj.get_component(GameCard)

        if game_card:
            self.process_card(game_card)

    def process_card(self, card):
        # if first line not empty we can't attack second
        if game_manager.is_enemy_card(self):
            if self.get_game_object().get_parent() == \
                    game_manager.enemy_second_line.get_game_object():
                if game_manager.enemy_first_line.get_game_object().child_count() > 0:
                    error_sound.play()
                    return

        # availability card
        if not card or not card.can_attack or card.attack_used:
            error_sound.play()
            return

        # we can't attack cards which in hand
        if not self.on_table:
            error_sound.play()
            return

        # friendly-fire is disabled
        if game_manager.is_enemy_card(self) and not game_manager.is_player_card(card):
            error_sound.play()
            return

        if game_manager.is_player_card(self) and not game_manager.is_enemy_card(card):
            error_sound.play()
            return

        # process fight
        game_manager.cards_fight(card, self)

        # disable attack
        card.attack_used = True

        # disable highlight
        card.get_game_object().get_child(highlight_index()).enabled = False

        # play sound
        fight_sound.play()

    def check_position(self):
        parent: Image = temp_card.get_parent()
        new_index = parent.child_count()

        for i in range(parent.child_count()):
            if self.get_game_object().get_global_position().x < \
                    parent.get_child(i).get_global_position().x:
                new_index = i

                if temp_card.get_sibling_index() < new_index:
                    new_index -= 1

                break

        temp_card.set_sibling_index(new_index)

    def turn_tick(self):
        if self.on_table:
            if not self.can_attack:
                self.can_attack = True
                self.get_game_object().get_child(highlight_index()).enabled = True

            if self.attack_used:
                self.attack_used = False
                self.get_game_object().get_child(highlight_index()).enabled = True
