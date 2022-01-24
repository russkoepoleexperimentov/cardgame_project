import sqlite3

from game import player_data_manager
from game.cards.card import CardInfo
from game.contstants import *

nations = set()
game_cards = list()
deck_by_nation = dict()
cards_by_nation = dict()
unlocked_cards_by_nation = dict()

player_id = 1


def init():
    # cards db
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cards_data = cur.execute(f"SELECT * FROM cards").fetchall()
    cur.close()
    con.close()

    # player_stats db
    player_data = player_data_manager.get_player_data()

    deck_data = {
        'soviet': player_data.get(PD_SOVIET_DECK),
        'germany': player_data.get(PD_GERMANY_DECK)
    }

    for card_data in cards_data:
        card_info = CardInfo(name=card_data[0],
                             icon_path=card_data[5],
                             card_type=card_data[7],
                             nation=card_data[6],
                             hit_points=card_data[1],
                             damage=card_data[2],
                             ammo_cost=card_data[3],
                             fuel_cost=card_data[4])

        game_cards.append(card_info)
        nations.add(card_info.nation)

        cards = cards_by_nation.get(card_info.nation, [])
        cards.append(card_info)
        cards_by_nation[card_info.nation] = cards

        if card_info.name in player_data.get(PD_UNLOCKED_CARDS):
            unl_cards = unlocked_cards_by_nation.get(card_info.nation, [])
            unl_cards.append(card_info)
            unlocked_cards_by_nation[card_info.nation] = unl_cards

        if card_info.name in deck_data[card_info.nation]:
            deck = deck_by_nation.get(card_info.nation, [])
            deck.append(card_info)
            deck_by_nation[card_info.nation] = deck


def check_in_deck(card_info: CardInfo):
    return card_info in deck_by_nation[card_info.nation]


def return_card_by_name(name):
    for card in game_cards:
        if card.name == name:
            return card


def save_cards_to_db():
    soviet_deck = [x.name for x in deck_by_nation['soviet']]
    germany_deck = [x.name for x in deck_by_nation['germany']]

    player_data_manager.get_player_data().update({PD_SOVIET_DECK: soviet_deck})
    player_data_manager.get_player_data().update({PD_GERMANY_DECK: germany_deck})
    player_data_manager.commit()
