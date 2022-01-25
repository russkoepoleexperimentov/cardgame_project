from core import scene_manager
from core.component import Component
from core.components.drag_handler import DragHandler
from core.resources import load_image
from core.ui.image import Image
from core.ui.text import Text
from core.vector import Vector
from game.cards.card import highlight_index
from game.contstants import HERO_HIT_POINTS
from core.components.drop_handler import DropHandler
from game.game_scene import game_manager
from game.game_scene.game_card import error_sound, GameCard, fight_sound
from scenes.game_end_scene import GameEndScene

HERO_ICON_PADDING = 5


class GameHero(Component):
    def __init__(self, owner: Image):
        super(GameHero, self).__init__(owner)
        self.drop_handler: DropHandler = owner.add_component(DropHandler)
        self.drop_handler.on_drop.add_listener(self.on_drop)

    def init(self, hero_data, is_player=False):
        self.hero_data = hero_data
        self.hit_points = HERO_HIT_POINTS

        padding = Vector(HERO_ICON_PADDING, HERO_ICON_PADDING)
        self.icon = Image(position=padding,
                          size=self.get_game_object().get_size() - padding * 2,
                          sprite=load_image(hero_data.icon_path))
        self.icon.block_raycasts = False
        self.icon.set_parent(self.get_game_object())

        self.hp_label = Text(position=Vector(0, self.get_game_object().get_size().y),
                             size=self.get_game_object().get_size(),
                             title=str(self.hit_points),
                             align='center')
        self.hp_label.block_raycasts = False
        self.hp_label.set_parent(self.get_game_object())

    def on_drop(self, drag: DragHandler):
            obj = drag.get_game_object()
            game_card: GameCard = obj.get_component(GameCard)

            if game_card:
                self.process_card(game_card)

    def process_card(self, card: GameCard):
        # if first line not empty we can't attack hero
        if game_manager.is_player_card(card):
            if game_manager.enemy_first_line.get_game_object().child_count() > 0:
                error_sound.play()
                return
        if game_manager.is_enemy_card(card):
            if game_manager.player_first_line.get_game_object().child_count() > 0:
                error_sound.play()
                return

        # availability card
        if not card or not card.can_attack or card.attack_used:
            error_sound.play()
            return

        # friendly-fire is disabled
        if self == game_manager.enemy_hero:
            if not game_manager.is_player_card(card):
                error_sound.play()
                return

        if self == game_manager.player_hero:
            if not game_manager.is_enemy_card(card):
                error_sound.play()
                return

        # decrease hp and update ui
        self.hit_points -= card.get_damage()
        self.hp_label.set_title(str(self.hit_points))

        # check for win
        if self.hit_points <= 0:
            if self == game_manager.enemy_hero:
                game_manager.game_result = game_manager.GR_PLAYER_WIN
            else:
                game_manager.game_result = game_manager.GR_ENEMY_WIN

        # disable attack
        card.attack_used = True

        # disable highlight
        if game_manager.is_player_card(card):
            card.get_game_object().get_child(highlight_index()).enabled = False

        # play sound
        fight_sound.play()
