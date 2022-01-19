import pygame

from core import config
from core.resources import load_image
from core.scene import Scene
from core.ui.button import Button
from core.ui.content_size_fitter import VerticalContentSizeFitter
from core.ui.image import Image
from core.ui.layout_group import GridLayoutGroup, HorizontalLayoutGroup
from core.ui.scroll_view import ScrollView
from core.ui.text import Text
from core.vector import Vector
from core.localization import translate_string
from game.button_sounds import ButtonSounds

from game.cards import card_manager

from game.contstants import BUTTON_DEFAULT_DESIGN
from game.cards.card import CARD_SIZE

from core import scene_manager

# buttons
BTN_SIZE = Vector(150, 30)
BTN_MARGIN = 5

# scroll view
SV_TOP_OFFSET = 150
SV_SIDE_OFFSET = 25
SV_BOTTOM_OFFSET = 30
SV_SLIDER_WIDTH = 20

# label
LABEL_HEIGHT = 50
LABEL_BOT_OFFSET = 20

# own deck board height
OWN_DECK_BOARD_HEIGHT = 1007 + LABEL_HEIGHT + LABEL_BOT_OFFSET

ALL_NATIONS = 'inter'


class DecksScene(Scene):
    def __init__(self):
        super(DecksScene, self).__init__()
        self.nations = (ALL_NATIONS, 'soviet', 'germany')
        self.screen_w, self.screen_h = tuple(map(int, config.get_value('vid_mode').split('x')))
        self.screen = Vector(self.screen_w, self.screen_h)

        background = Image(size=self.screen, sprite=load_image('sprites/ui/menu_blur.png'))
        self.add_game_object(background, -100)

        back_btn = Button(**BUTTON_DEFAULT_DESIGN,
                          position=Vector(40, 30),
                          size=BTN_SIZE,
                          title=translate_string('ui.back'))
        back_btn.add_component(ButtonSounds)
        back_btn.on_click.add_listener(self.load_menu)
        back_btn.label.set_font_size(25)
        self.add_game_object(back_btn, 150)

        self.switch_buttons_group = None
        self.scroll_view = None

        self.chosen_nation = ''

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

        nations = sorted(card_manager.game_cards)

        self.nation_buttons = dict()

        for nation in nations:
            btn = Button(**BUTTON_DEFAULT_DESIGN, size=BTN_SIZE, title=translate_string(nation))
            btn.set_parent(self.switch_buttons_group)
            btn.add_component(ButtonSounds)
            btn.label.set_font_size(20)
            btn.on_click.add_listener(lambda n=nation: self.show_nation(n))
            self.nation_buttons[nation] = btn

        if len(nations) > 0:
            self.show_nation(nations[0])

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

        content_offset = Vector(90, 50)

        self.other_cards_parent = Image(size=Vector(self.scroll_view.get_size().x, 0),
                                        position=content_offset + Vector(0, OWN_DECK_BOARD_HEIGHT))
        self.other_cards_parent.set_parent(self.scroll_view.content)
        content_size_fitter = self.other_cards_parent.add_component(VerticalContentSizeFitter)
        content_size_fitter.after_space = 100

        layout_group = self.other_cards_parent.add_component(GridLayoutGroup)
        layout_group.cell_size = CARD_SIZE
        layout_group.spacing = 25

        self.scroll_view.slider.set_value(0)
        self.other_cards_parent.set_size(self.other_cards_parent.get_size() - content_offset * 2)

        own_deck_background = Image(size=Vector(self.scroll_view.content.get_size().x,
                                                OWN_DECK_BOARD_HEIGHT),
                                    sprite=load_image('sprites/ui/my_deck_background.jpg'))
        own_deck_background.set_parent(self.scroll_view.content)

        self.deck_cards_parent = Image(size=Vector(self.scroll_view.content.get_size().x -
                                                   content_offset.x * 2, 1),
                                       position=content_offset + Vector(0, LABEL_HEIGHT +
                                                                        LABEL_BOT_OFFSET))
        self.deck_cards_parent.set_parent(own_deck_background)

        self.other_cards_parent.position = content_offset + Vector(0, OWN_DECK_BOARD_HEIGHT)

        content_size_fitter = self.deck_cards_parent.add_component(VerticalContentSizeFitter)
        content_size_fitter.after_space = 100

        layout_group = self.deck_cards_parent.add_component(GridLayoutGroup)
        layout_group.cell_size = CARD_SIZE
        layout_group.spacing = 25

        label = Text(position=Vector(0, 50),
                     size=Vector(self.screen_w, LABEL_HEIGHT),
                     title=translate_string('ui.own_decks'),
                     align='center',
                     valign='middle',
                     font_size=72)
        label.set_parent(own_deck_background)

    def show_nation(self, nation: str):
        self.clear_scroll_view()
        self.chosen_nation = nation

        for button in self.nation_buttons.values():
            button.interactable = True
        self.nation_buttons[nation].interactable = False

        cards = card_manager.game_cards.get(nation, [])
        deck_cards = list(filter(lambda x: x.in_deck == 'True', cards))
        other_cards = list(filter(lambda x: x.in_deck == 'False', cards))

        for card_info in deck_cards:
            card_obj = card_info.build_card_object()
            card_obj.set_parent(self.deck_cards_parent)

        for card_info in other_cards:
            card_obj = card_info.build_card_object()
            card_obj.set_parent(self.other_cards_parent)

    def clear_scroll_view(self):
        for child in self.deck_cards_parent.get_children():
            child.set_parent(None)
            del child
        for child in self.other_cards_parent.get_children():
            child.set_parent(None)
            del child
        self.scroll_view.slider.set_value(0)

    def event_hook(self, event):
        super().event_hook(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.load_menu()

    def load_menu(self):
        from scenes.menu import MenuScene
        scene_manager.load(MenuScene())
