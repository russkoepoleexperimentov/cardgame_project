import sqlite3

from game.cards.card import CardInfo
from game.contstants import DATABASE, PLAYER_STATS_BASE

nations = set()
game_cards = list()
deck_by_nation = dict()
cards_by_nation = dict()

player_id = 1


def init():
    # cards db
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cards_data = cur.execute(f"SELECT * FROM cards").fetchall()
    cur.close()
    con.close()

    # player_stats db
    con = sqlite3.connect(PLAYER_STATS_BASE)
    cur = con.cursor()
    player_data = cur.execute(f"""SELECT * FROM player_stats 
    WHERE player_id = '{player_id}'""").fetchall()[0]
    cur.close()
    con.close()

    SEP = ', '
    soviet_deck, germany_deck, unlocked_cards = map(lambda t: t.split(SEP), player_data[1:4])
    deck_data = {
        'soviet': soviet_deck,
        'germany': germany_deck
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

        if card_info.name in deck_data[card_info.nation]:
            deck = deck_by_nation.get(card_info.nation, [])
            deck.append(card_info)
            deck_by_nation[card_info.nation] = deck


def check_in_deck(card_info: CardInfo):
    return card_info in deck_by_nation[card_info.nation]


def save_cards_to_db():
    soviet_deck = ', '.join([x.name for x in deck_by_nation['soviet']])
    germany_deck = ', '.join([x.name for x in deck_by_nation['germany']])

    con = sqlite3.connect(PLAYER_STATS_BASE)
    cur = con.cursor()
    cur.execute(f"""UPDATE player_stats SET soviet_deck = '{soviet_deck}',
    germany_deck = '{germany_deck}' WHERE player_id = '{player_id}'""")
    con.commit()
    cur.close()
    con.close()
