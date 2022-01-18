import sqlite3

from core.localization import translate_string
from core.ui.image import Image
from core.ui.text import Text
from core.vector import Vector
from core.resources import load_image

from game.contstants import DATABASE

CARD_WIDTH = 200
CARD_SCALE = CARD_WIDTH / 720

CARD_ASPECT_RATIO = 0.7
CARD_SIZE = Vector(CARD_WIDTH, CARD_WIDTH / CARD_ASPECT_RATIO)

CARD_ICON_SIZE = Vector(721 * CARD_SCALE, 765 * CARD_SCALE)
CARD_ICON_POSITION = Vector(0, 173 * CARD_SCALE)

TEXT_NAME_POS, TEXT_NAME_SIZE = Vector(157 * CARD_SCALE, 0), Vector(407 * CARD_SCALE,
                                                                    102 * CARD_SCALE)
TEXT_NAME_FONT_SIZE = 18

COST_TEXT_TOP = 65 * CARD_SCALE
COST_TEXT_SIZE = Vector(130 * CARD_SCALE, 100 * CARD_SCALE)

BOTTOM_TEXT_SIZE = Vector(360 * CARD_SCALE, 100 * CARD_SCALE)
BOTTOM_TEXT_POS = Vector(0, 937 * CARD_SCALE)

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
        card_back = Image(size=CARD_SIZE,
                          sprite=load_image('sprites/card_face_back.png'))

        card_icon = Image(size=CARD_ICON_SIZE,
                          sprite=load_image(self.icon_path),
                          position=CARD_ICON_POSITION)
        card_icon.set_parent(card_back)

        card_face = Image(size=CARD_SIZE,
                          sprite=load_image('sprites/card_face.png'))
        card_face.set_parent(card_back)

        card_name = Text(position=TEXT_NAME_POS,
                         size=TEXT_NAME_SIZE,
                         title=translate_string(self.name),
                         align='center',
                         valign='middle')
        card_name.set_font_size(TEXT_NAME_FONT_SIZE)
        card_name.set_parent(card_back)

        card_ammo_cost = Text(position=Vector(0, COST_TEXT_TOP),
                              size=COST_TEXT_SIZE,
                              title=translate_string(str(self.ammo_cost)),
                              align='right',
                              valign='bottom')
        card_ammo_cost.set_parent(card_back)

        card_fuel_cost = Text(position=Vector(564 * CARD_SCALE, COST_TEXT_TOP),
                              size=COST_TEXT_SIZE,
                              title=translate_string(str(self.fuel_cost)),
                              align='right',
                              valign='bottom')
        card_fuel_cost.set_parent(card_back)

        card_type = Text(position=BOTTOM_TEXT_POS,
                         size=BOTTOM_TEXT_SIZE,
                         title=translate_string(self.type),
                         align='center',
                         valign='middle')
        card_type.set_parent(card_back)

        card_description = Text(position=BOTTOM_TEXT_POS + Vector(BOTTOM_TEXT_SIZE.x, 0),
                                size=BOTTOM_TEXT_SIZE,
                                title=translate_string(self.description),
                                align='center',
                                valign='middle')
        card_description.set_parent(card_back)
        return card_back
