from core import application
from game.cards import card_manager
from server_core.server_resources import CardInfo


def switch_cards(nation, in_deck: CardInfo, other: CardInfo):
    if in_deck.nation != nation or other.nation != nation:
        raise ValueError()

    deck: list = card_manager.deck_by_nation[nation]

    in_deck_index = deck.index(in_deck.section)
    deck.remove(in_deck.section)
    deck.insert(in_deck_index, other.section)
    application.client.send_packet(('switch_deck_card', other.section, in_deck.section, nation))
    # card_manager.save_cards_to_db()
