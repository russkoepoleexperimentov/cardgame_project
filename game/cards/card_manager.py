import sqlite3

from core import application
from game import player_data_manager
from game.cards.hero_data import HeroData
from game.contstants import *
from server_core.server_resources import CardInfo

nations = set()
game_cards = dict()
deck_by_nation = dict()
cards_by_nation = dict()
hero_by_nation = dict()
unlocked_cards_by_nation = dict()


def register_cards(cards):
    nations.clear()
    game_cards.clear()
    deck_by_nation.clear()
    cards_by_nation.clear()
    unlocked_cards_by_nation.clear()
    hero_by_nation.clear()

    for card_info in cards:
        game_cards[card_info.name] = card_info
        nations.add(card_info.nation)

        cards = cards_by_nation.get(card_info.nation, [])
        cards.append(card_info)
        cards_by_nation[card_info.nation] = cards

    application.client.send_packet(('get_unlocked_cards',))


def on_packet(name, *data):
    print('received', name)
    if name == 'decks_response':
        deck_by_nation.update(data[0])
    if name == 'unlocked_cards_response':
        for n in nations:
            unlocked_cards_by_nation[n] = []
        for card_name in data[0]:
            card = game_cards[card_name]
            nation = unlocked_cards_by_nation.get(card.nation, [])
            nation.append(card)
            unlocked_cards_by_nation.update({card.nation: nation})
        print('unl', unlocked_cards_by_nation)
        application.client.send_packet(('get_decks',))


application.client.on_packet.add_listener(on_packet)


def check_in_deck(card_info: CardInfo):
    return card_info in deck_by_nation[card_info.nation]


def return_card_by_name(name):
    return game_cards[name]


def save_cards_to_db():
    return
    soviet_deck = [x.name for x in deck_by_nation['soviet']]
    germany_deck = [x.name for x in deck_by_nation['germany']]

    player_data_manager.get_player_data().update({PD_SOVIET_DECK: soviet_deck})
    player_data_manager.get_player_data().update({PD_GERMANY_DECK: germany_deck})
    player_data_manager.commit()