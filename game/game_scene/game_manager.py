from random import sample

from game.cards import card_manager
from game.game_scene.card_line import CardLine

player_first_line: CardLine = None
player_second_line: CardLine = None
player_hand: CardLine = None
enemy_first_line: CardLine = None
enemy_second_line: CardLine = None
enemy_hand: CardLine = None

player_deck = []
enemy_deck = []


def get_player_deck():
    return player_deck


def get_enemy_deck():
    return enemy_deck


turn_count = 0


def init_decks(player: str, enemy: str):
    global player_deck, enemy_deck
    player_deck = list(card_manager.deck_by_nation.get(player))
    enemy_deck = sample(list(card_manager.cards_by_nation.get(enemy)), k=15)


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
