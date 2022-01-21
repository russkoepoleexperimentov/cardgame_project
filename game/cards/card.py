import sqlite3

from core.localization import translate_string
from core.ui.image import Image
from core.ui.text import Text
from core.vector import Vector
from core.resources import load_image

from game.contstants import DATABASE


class CardInfo:
    def __init__(self,
                 name: str,
                 icon_path: str,
                 card_type: str,
                 nation: str,
                 hit_points: int,
                 damage: int,
                 ammo_cost: int,
                 fuel_cost: int):
        self.name = name
        self.icon_path = icon_path
        self.type = card_type
        self.nation = nation
        self.hit_points = hit_points
        self.damage = damage
        self.ammo_cost = ammo_cost
        self.fuel_cost = fuel_cost

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def build_card_object(self, card_width=200):
        card_scale = card_width / 720

        card_aspect_ratio = 0.7
        card_size = Vector(card_width, card_width / card_aspect_ratio)

        card_icon_size = Vector(721 * card_scale, 765 * card_scale)
        card_icon_position = Vector(0, 173 * card_scale)

        text_name_pos, text_name_size = Vector(157 * card_scale, 0), Vector(407 * card_scale,
                                                                            102 * card_scale)

        cost_text_top = 65 * card_scale
        cost_text_size = Vector(130 * card_scale, 100 * card_scale)

        bottom_text_size = Vector(360 * card_scale, 100 * card_scale)
        bottom_text_pos = Vector(0, 937 * card_scale)

        damage_hp_text_size = Vector(175 * card_scale, 67 * card_scale)
        damage_hp_text_font_size = int(70 * card_scale)
        hp_text_pos = Vector(371 * card_scale, 104 * card_scale)
        damage_text_pos = Vector(157 * card_scale, 104 * card_scale)

        card_back = Image(size=card_size,
                          sprite=load_image('sprites/card_face_back.png'))

        card_icon = Image(size=card_icon_size,
                          sprite=load_image(self.icon_path),
                          position=card_icon_position)
        card_icon.set_parent(card_back)
        card_icon.block_raycasts = False

        card_face = Image(size=card_size,
                          sprite=load_image('sprites/card_face.png'))
        card_face.set_parent(card_back)
        card_face.block_raycasts = False

        card_name = Text(position=text_name_pos,
                         size=text_name_size,
                         title=translate_string(self.name),
                         align='center',
                         valign='middle',
                         font_size=int(80 * card_scale))
        card_name.set_parent(card_back)
        card_name.block_raycasts = False

        card_ammo_cost = Text(position=Vector(0, cost_text_top),
                              size=cost_text_size,
                              title=translate_string(str(self.ammo_cost)),
                              align='right',
                              valign='bottom',
                              font_size=int(108 * card_scale))
        card_ammo_cost.set_parent(card_back)
        card_ammo_cost.block_raycasts = False

        card_fuel_cost = Text(position=Vector(564 * card_scale, cost_text_top),
                              size=cost_text_size,
                              title=translate_string(str(self.fuel_cost)),
                              align='right',
                              valign='bottom',
                              font_size=int(108 * card_scale))
        card_fuel_cost.set_parent(card_back)
        card_fuel_cost.block_raycasts = False

        card_type = Text(position=bottom_text_pos,
                         size=bottom_text_size,
                         title=translate_string(self.type),
                         align='center',
                         valign='middle',
                         font_size=int(70 * card_scale))
        card_type.set_parent(card_back)
        card_type.block_raycasts = False

        card_hit_points = Text(position=hp_text_pos,
                               size=damage_hp_text_size,
                               title=str(self.hit_points),
                               align='right',
                               valign='middle',
                               font_size=damage_hp_text_font_size)
        card_hit_points.set_parent(card_back)
        card_hit_points.block_raycasts = False

        card_damage = Text(position=damage_text_pos,
                           size=damage_hp_text_size,
                           title=str(self.damage),
                           align='right',
                           valign='middle',
                           font_size=damage_hp_text_font_size)
        card_damage.set_parent(card_back)
        card_damage.block_raycasts = False
        print(card_hit_points.get_sibling_index(), card_damage.get_sibling_index())

        return card_back
