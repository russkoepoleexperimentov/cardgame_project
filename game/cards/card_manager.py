import sqlite3

from game.cards.card import CardInfo
from game.contstants import DATABASE

nations = set()
game_cards = list()


def init():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cards_data = cur.execute(f"SELECT * FROM cards").fetchall()
    cur.close()
    con.close()
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
    """con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        card_data = cur.execute(f"SELECT * FROM cards WHERE name = '{name}'").fetchall()[0]
        self.name = name
        self.hit_points = card_data[1]
        self.damage = card_data[2]
        self.ammo_cost = card_data[3]
        self.fuel_cost = card_data[4]
        self.icon_path = card_data[5]
        self.nation = card_data[6]
        self.type = card_data[7]
        self.unlock = card_data[8]
        cur.close()
        con.close()
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    nations = set([x[0] for x in cur.execute(f"SELECT nation FROM cards").fetchall()])
    nations = list(nations)
    nations.sort()

    cur.close()
    con.close()

    for nation in nations:
        btn = Button(**BUTTON_DEFAULT_DESIGN, size=BTN_SIZE, title=translate_string(nation))
        btn.set_parent(self.switch_buttons_group)
        btn.add_component(ButtonSounds)
        btn.label.set_font_size(20)

        btn.on_click.add_listener(lambda n=nation: self.show_nation(n))"""
