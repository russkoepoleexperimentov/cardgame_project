import sqlite3
from core import config
from game.contstants import DATABASE, BUTTON_DEFAULT_DESIGN, BUTTONS_SIZE
from core.resources import load_image
from core.scene import Scene
from core.ui.button import Button
from core.ui.image import Image
from core.ui.text import Text
from core.vector import Vector
from core.localization import translate_string
from game.button_sounds import ButtonSounds
from game.cards import card_manager
from core import scene_manager
from scenes.menu import MenuScene
from random import choice


class ChestsScene(Scene):
    def __init__(self):
        super(ChestsScene, self).__init__()
        self.card_on_screen = False
        con = sqlite3.connect(DATABASE)
        self.cur = con.cursor()
        self.screen_w, self.screen_h = tuple(map(int, config.get_value('vid_mode').split('x')))
        self.screen = Vector(self.screen_w, self.screen_h)
        background = Image(size=self.screen, sprite=load_image('sprites/ui/menu_blur.png'))
        self.add_game_object(background, -100)
        back_btn = Button(**BUTTON_DEFAULT_DESIGN, position=Vector(40, 30), size=Vector(150, 30),
                          title=translate_string('ui.back'))
        back_btn.add_component(ButtonSounds)
        back_btn.on_click.add_listener(self.load_menu)
        back_btn.label.set_font_size(25)
        self.add_game_object(back_btn, 150)
        chest = Image(sprite=load_image('sprites/ui/chest.png'), size=Vector(400, 400),
                      position=Vector(30, 120))
        self.add_game_object(chest)
        self.chest_count = self.cur.execute('SELECT chests_count FROM player_stats').fetchall()[0][0]
        chest_info = Text(position=Vector(60, 550), size=BUTTONS_SIZE,
                          title=translate_string('ui.chest_info') + ': ' + str(self.chest_count))
        self.add_game_object(chest_info)
        open_btn = Button(**BUTTON_DEFAULT_DESIGN, position=Vector(60, 580), size=BUTTONS_SIZE,
                          title=translate_string('ui.open'))
        open_btn.add_component(ButtonSounds)
        open_btn.on_click.add_listener(self.open_chest)
        self.add_game_object(open_btn)

    def open_chest(self):
        claim_info = Text(position=Vector(200, 120), size=BUTTONS_SIZE,
                          title=translate_string('ui.congratulations') + ':')
        self.add_game_object(claim_info)
        lock_cards = self.cur.execute('SELECT * FROM cards WHERE unlock = "False"').fetchall()[0]
        random_card_name = choice(lock_cards)


    def load_menu(self):
        scene_manager.load(MenuScene())
