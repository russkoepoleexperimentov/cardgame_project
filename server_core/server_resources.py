import os
import sqlite3

_global_resources = None


def global_resources():
    return _global_resources


class ServerResources:
    def __init__(self, working_dir):
        self._nations = set()
        self._cards = []
        self._bases = dict()
        self._base_decks = dict()

        global _global_resources
        _global_resources = self

        db = os.path.join(working_dir, 'data/cards.sqlite3')
        con = sqlite3.connect(db)
        cur = con.cursor()
        default_decks_data = cur.execute('SELECT * FROM base_cards').fetchall()
        cards_data = cur.execute('SELECT * FROM cards').fetchall()
        bases_data = cur.execute('SELECT * FROM heroes').fetchall()
        cur.close()
        con.close()

        for nation, cards in default_decks_data:
            cards = cards.split(',')
            cards = list(map(lambda x: x.strip(), cards))
            self._base_decks.update({nation: cards})

        for card_data in cards_data:
            card_info = CardInfo(display_name=card_data[0],
                                 icon_path=card_data[5],
                                 card_type=card_data[7],
                                 nation=card_data[6],
                                 hit_points=card_data[1],
                                 damage=card_data[2],
                                 ammo_cost=card_data[3],
                                 fuel_cost=card_data[4],
                                 section=card_data[8])

            self._cards.append(card_info)
            self._nations.add(card_info.nation)

        for base_data in bases_data:
            base_info = BaseInfo(name=base_data[0],
                                 nation=base_data[1],
                                 icon_path=base_data[2])
            self._bases.update({base_info.nation: base_info})

    def cards_by_nation(self, nation_name: str):
        if nation_name not in self._nations:
            raise ReferenceError

        return tuple(filter(lambda c: c.nation == nation_name, self._cards))

    def card_by_section(self, section: str):
        for card in self._cards:
            if card.section == section:
                return card
        return None

    def cards(self):
        return tuple(self._cards)

    def card_sections(self):
        return tuple(map(lambda x: x.section, self._cards))

    def cards_tuple(self):
        return tuple(map(lambda x: x.to_tuple(), self._cards))

    def nations(self):
        return tuple(self._nations)

    def base(self, nation):
        return self._bases.get(nation, None)

    def get_base_decks(self):
        return dict(self._base_decks)


class CardInfo:
    def __init__(self,
                 display_name: str,
                 icon_path: str,
                 card_type: str,
                 nation: str,
                 hit_points: int,
                 damage: int,
                 ammo_cost: int,
                 fuel_cost: int,
                 section: str):
        self.display_name = display_name
        self.icon_path = icon_path
        self.type = card_type
        self.nation = nation
        self.hit_points = hit_points
        self.damage = damage
        self.ammo_cost = ammo_cost
        self.fuel_cost = fuel_cost
        self.section = section

    def to_tuple(self):
        return (self.display_name, self.icon_path, self.type, self.nation, self.hit_points,
                self.damage, self.ammo_cost, self.fuel_cost, self.section)


class BaseInfo:
    def __init__(self,
                 name: str,
                 icon_path: str,
                 nation: str):
        self.name = name
        self.icon_path = icon_path
        self.nation = nation