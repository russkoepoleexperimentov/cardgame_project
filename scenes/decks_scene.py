from core import config
from core.resources import load_image
from core.scene import Scene
from core.ui.button import Button
from core.ui.image import Image
from core.ui.layout_group import GridLayoutGroup, HorizontalLayoutGroup
from core.ui.scroll_view import ScrollView
from core.ui.text import Text
from core.vector import Vector
from core.localization import translate_string
from game.button_sounds import ButtonSounds

from game.card import Card

from game.contstants import BUTTON_DEFAULT_DESIGN, DATABASE

import sqlite3

# buttons
BTN_SIZE = Vector(150, 30)
BTN_MARGIN = 5

# scroll view
SV_TOP_OFFSET = 100
SV_SIDE_OFFSET = 25
SV_BOTTOM_OFFSET = 30
SV_SLIDER_WIDTH = 20

ALL_NATIONS = 'inter'


class DecksScene(Scene):
    def __init__(self):
        super(DecksScene, self).__init__()
        self.screen_w, self.screen_h = tuple(map(int, config.get_value('vid_mode').split('x')))
        self.screen = Vector(self.screen_w, self.screen_h)

        background = Image(size=self.screen, sprite=load_image('sprites/ui/menu.png'))
        self.add_game_object(background, -100)

        label = Text(size=Vector(self.screen_w, 50),
                     title='Личные колоды',
                     align='center',
                     valign='middle',
                     font_size=72)
        label.set_parent(background)

        self.init_scroll_view()
        self.init_switch_buttons()

    def init_switch_buttons(self):
        self.switch_buttons_group = Image(size=Vector(self.screen_w - 2 * SV_SIDE_OFFSET -
                                                      SV_SLIDER_WIDTH,
                                                      BTN_SIZE.y),
                                          position=Vector(SV_SIDE_OFFSET, SV_TOP_OFFSET -
                                                          BTN_SIZE.y - BTN_MARGIN))
        self.add_game_object(self.switch_buttons_group)
        horizontal_layout_group = self.switch_buttons_group.add_component(HorizontalLayoutGroup)
        horizontal_layout_group.spacing = BTN_MARGIN

        # DATABASE
        '''con = sqlite3.connect(DATABASE)
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

            def click():
                self.show_nation(nation)
                print(nation)
            btn.on_click.add_listener(click)

        if len(nations) > 0:
            self.show_nation(nations[0])'''

        nations = [ALL_NATIONS, 'soviet', 'germany']
        btns = []

        for i in range(len(nations)):
            nation = nations[i]
            btn = Button(**BUTTON_DEFAULT_DESIGN, size=BTN_SIZE, title=translate_string(nation))
            btn.on_click.add_listener(lambda: self.show_nation(nations[i]))
            btn.set_parent(self.switch_buttons_group)
            btn.add_component(ButtonSounds)
            btn.label.set_font_size(20)
            btns.append(btn)

       # btns[0].on_click.add_listener(lambda: self.show_nation(nations[0]))
       # btns[1].on_click.add_listener(lambda: self.show_nation(nations[1]))
       # btns[2].on_click.add_listener(lambda: self.show_nation(nations[2]))


    def init_scroll_view(self):
        self.scroll_view = ScrollView(size=Vector(self.screen_w - 2 * SV_SIDE_OFFSET -
                                                  SV_SLIDER_WIDTH,
                                                  self.screen_h - SV_TOP_OFFSET - SV_BOTTOM_OFFSET),
                                      position=Vector(SV_SIDE_OFFSET, SV_TOP_OFFSET),
                                      background_sprite=
                                      load_image('sprites/ui/scroll_view_back.png'),
                                      slider_background_sprite=
                                      load_image('sprites/ui/slider_back.png'),
                                      slider_handle_sprite=
                                      load_image('sprites/ui/slider_handle.png'),
                                      slider_width=SV_SLIDER_WIDTH)
        self.add_game_object(self.scroll_view)

        content = self.scroll_view.content
        layout_group = content.add_component(GridLayoutGroup)
        layout_group.cell_size = Vector(90, 100)
        layout_group.spacing = 10
        self.scroll_view.content_offset = Vector(10, 10)
        self.scroll_view.slider.set_value(0)
        content.set_size(content.get_size() - Vector(10, 10) * 2)

    def show_nation(self, nation: str):

        print(nation)
        self.clear_scroll_view()

        con = sqlite3.connect(DATABASE)
        cur = con.cursor()

        if nation == ALL_NATIONS:
            query = f"SELECT name FROM cards"
        else:
            query = f"SELECT name FROM cards WHERE nation = '{nation}'"

        cards_names = cur.execute(query).fetchall()

        cur.close()
        con.close()

        for name in cards_names:
            name = name[0]
            card = Card(name)
            card_obj = card.create_card()
            card_obj.set_parent(self.scroll_view.content)

    def clear_scroll_view(self):
        for child in self.scroll_view.content.get_children():
            child.set_parent(None)
            del child