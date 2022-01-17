import sqlite3

from core.localization import translate_string
from core.ui.image import Image
from core.ui.text import Text
from core.vector import Vector
from core.resources import load_image

from game.contstants import DATABASE


class Card:
    def __init__(self, name):
        con = sqlite3.connect(DATABASE)
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
        self.description = 'desc'#cur.execute(f"SELECT description FROM types WHERE type = '{self.type}'").fetchall()[0][0]
        cur.close()
        con.close()

    def create_card(self):
        card_face = Image(size=Vector(150, 250), sprite=load_image('sprites/card_face.jpg'))
        card_icon = Image(size=Vector(150, 300), sprite=load_image(self.icon_path),
                          position=Vector(0, 50))
        card_icon.set_parent(card_face)
        card_name = Text(size=Vector(150, 25), title=translate_string(self.name), align='center',
                         valign='middle')
        card_name.set_parent(card_face)
        card_ammo_cost = Text(size=Vector(25, 25), title=translate_string(str(self.ammo_cost)),
                              align='center', valign='middle')
        card_ammo_cost.set_parent(card_face)
        if self.fuel_cost != 0:
            card_fuel_cost = Text(size=Vector(25, 25), title=translate_string(str(self.fuel_cost)),
                                  align='center', valign='middle', position=Vector(125, 0))
            card_fuel_cost.set_parent(card_face)
        card_type = Text(size=Vector(75, 50), title=translate_string(self.type), align='center',
                         valign='middle', position=Vector(0, 350))
        card_type.set_parent(card_face)
        card_description = Text(size=Vector(75, 50), title=translate_string(self.description),
                                align='center', valign='middle', position=Vector(75, 350))
        card_description.set_parent(card_face)
        return card_face
