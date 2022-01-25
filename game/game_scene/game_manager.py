from random import sample

from core.ui.layout_group import LayoutGroup
from game.cards import card_manager
from game.cards.hero_data import HeroData
from game.game_scene.card_line import CardLine
from game.game_scene.game_hero import GameHero

player_first_line: CardLine = None
player_second_line: CardLine = None
player_hand: CardLine = None
enemy_first_line: CardLine = None
enemy_second_line: CardLine = None
enemy_hand: CardLine = None

player_ammo = 0
player_fuel = 0

enemy_ammo = 0
enemy_fuel = 0

ui_player_ammo = None
ui_player_fuel = None

player_deck = []
enemy_deck = []
player_nation: str = None
enemy_nation: str = None
player_hero: GameHero = None
enemy_hero: GameHero = None

GR_PLAYER_WIN = 'PLAYER_WIN'
GR_ENEMY_WIN = 'ENEMY_WIN'
game_result = ''


def get_player_deck():
    return player_deck


def get_enemy_deck():
    return enemy_deck


def refresh_card_parents():
    parents = (enemy_first_line,
               enemy_second_line,
               player_first_line,
               player_second_line,
               player_hand,
               enemy_hand)

    for p in parents:
        if p:
            layout_group = p.get_game_object().get_component(LayoutGroup)
            if layout_group:
                layout_group.refresh()


turn_count = 0


def init_decks(player: str, enemy: str):
    global player_deck, enemy_deck, player_nation, enemy_nation
    player_deck = list(card_manager.deck_by_nation.get(player))
    enemy_deck = sample(list(card_manager.cards_by_nation.get(enemy)), k=15)
    player_nation = player
    enemy_nation = enemy


def is_player_card(card):
    return card.get_game_object() in player_first_line.get_game_object().get_children() or \
           card.get_game_object() in player_second_line.get_game_object().get_children() or \
           card.get_game_object() in player_hand.get_game_object().get_children()


def is_enemy_card(card):
    return card.get_game_object().get_parent() == enemy_first_line.get_game_object() or \
           card.get_game_object().get_parent() == enemy_second_line.get_game_object() or \
           card.get_game_object().get_parent() == enemy_hand.get_game_object()


def enemy_turn():
    if player_first_line.get_game_object().get_children():
        # attack first line
        pass
    else:
        # attack second line
        pass

    end_turn()


def is_player_turn():
    return turn_count % 2 == 0


def get_turn_count():
    return turn_count


def end_turn():
    global turn_count
    turn_count += 1


def cards_fight(card1, card2):
    card1.decrease_hit_points(card2.get_damage())
    card2.decrease_hit_points(card1.get_damage())
