import sqlite3

from game import player_data_manager
from game.cards.card import CardInfo
from game.cards.hero_data import HeroData
from game.contstants import *

nations = set()
game_cards = list()
deck_by_nation = dict()
cards_by_nation = dict()
hero_by_nation = dict()
unlocked_cards_by_nation = dict()

player_id = 1


def init():
    nations.clear()
    game_cards.clear()
    deck_by_nation.clear()
    cards_by_nation.clear()
    unlocked_cards_by_nation.clear()
    hero_by_nation.clear()

    # cards db
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cards_data = cur.execute(f"SELECT * FROM cards").fetchall()
    heroes_data = cur.execute(f"SELECT * FROM heroes").fetchall()
    cur.close()
    con.close()

    # player_stats db
    player_data = player_data_manager.get_player_data()

    deck_data = player_data_manager.get_player_data()

    for card_data in cards_data:
        card_info = CardInfo(display_name=card_data[0],
                             icon_path=card_data[5],
                             card_type=card_data[7],
                             nation=card_data[6],
                             hit_points=card_data[1],
                             damage=card_data[2],
                             ammo_cost=card_data[3],
                             fuel_cost=card_data[4],
                             section=card_data[8],
                             description=card_data[9])

        game_cards.append(card_info)
        nations.add(card_info.nation)

        cards = cards_by_nation.get(card_info.nation, [])
        cards.append(card_info)
        cards_by_nation[card_info.nation] = cards

        if card_info.section in player_data.get(PD_UNLOCKED_CARDS):
            unl_cards = unlocked_cards_by_nation.get(card_info.nation, [])
            unl_cards.append(card_info)
            unlocked_cards_by_nation[card_info.nation] = unl_cards

        if card_info.section in deck_data[card_info.nation]:
            deck = deck_by_nation.get(card_info.nation, [])
            deck.append(card_info)
            deck_by_nation[card_info.nation] = deck

    for hero_data in heroes_data:
        hero_info = HeroData(name=hero_data[0],
                             nation=hero_data[1],
                             icon_path=hero_data[2])
        hero_by_nation.update({hero_info.nation: hero_info})


def check_in_deck(card_info: CardInfo):
    return card_info in deck_by_nation[card_info.nation]


def return_card_by_name(name):
    for card in game_cards:
        if card.name == name:
            return card


def save_cards_to_db():
    for nation in nations:
        player_data_manager.get_player_data()\
            .update({nation: [x.section for x in deck_by_nation[nation]]})

    player_data_manager.commit()
