from game.cards import card_manager
from server_core.server_resources import CardInfo


def switch_cards(nation, in_deck: CardInfo, other: CardInfo):
    if in_deck.nation != nation or other.nation != nation:
        raise ValueError()

    deck: list = card_manager.deck_by_nation[nation]

    in_deck_index = deck.index(in_deck)
    deck.remove(in_deck)
    deck.insert(in_deck_index, other)
    card_manager.save_cards_to_db()
