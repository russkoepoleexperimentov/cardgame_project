from core import config, scene_manager
from core.component import Component
from core.localization import translate_string
from core.resources import load_image
from core.ui.button import Button
from core.ui.content_size_fitter import VerticalContentSizeFitter
from core.ui.image import Image
from core.ui.layout_group import GridLayoutGroup
from core.ui.scroll_view import ScrollView
from core.ui.text import Text
from core.vector import Vector
from game.cards import card_manager
from game.contstants import BUTTON_DEFAULT_DESIGN
from game.decks_scene import card_switcher


# scroll view
from game.decks_scene.card_click_handler import CardClickHandler

SV_TOP_OFFSET = 150
SV_SIDE_OFFSET = 25
SV_BOTTOM_OFFSET = 30
SV_SLIDER_WIDTH = 20

CONTENT_OFFSET = Vector(90, 50)

# label
LABEL_HEIGHT = 50
LABEL_BOT_OFFSET = 20

# own deck board height
OWN_DECK_BOARD_HEIGHT = 1007 + LABEL_HEIGHT + LABEL_BOT_OFFSET


class CardsList(Component):
    def __init__(self, owner: ScrollView):
        super(CardsList, self).__init__(owner)

        self.scroll_view = owner
        self.screen_w, self.screen_h = tuple(map(int, config.get_value('vid_mode').split('x')))
        self.screen = Vector(self.screen_w, self.screen_h)
        self.nation_buttons = None

        # vars for swap cards
        self.card_swapping = False

        # deck cards parent
        deck_background = Image(size=Vector(self.scroll_view.content.get_size().x,
                                            OWN_DECK_BOARD_HEIGHT),
                                sprite=load_image('sprites/ui/my_deck_background.jpg'))
        deck_background.set_parent(self.scroll_view.content)

        card_parent_size = Vector(self.scroll_view.content.get_size().x - CONTENT_OFFSET.x * 2, 1)

        self.deck_cards_parent = Image(size=card_parent_size,
                                       position=CONTENT_OFFSET + Vector(0, LABEL_HEIGHT +
                                                                        LABEL_BOT_OFFSET))
        self.deck_cards_parent.set_parent(deck_background)

        content_size_fitter = self.deck_cards_parent.add_component(VerticalContentSizeFitter)
        content_size_fitter.after_space = 100

        layout_group = self.deck_layouts_group = \
            self.deck_cards_parent.add_component(GridLayoutGroup)
        layout_group.cell_size = Vector(200, 200 / 0.7)
        layout_group.spacing = 25

        # other cards parent
        self.other_cards_parent = Image(size=card_parent_size,
                                        position=CONTENT_OFFSET + Vector(0, OWN_DECK_BOARD_HEIGHT) +
                                                 Vector(0, LABEL_HEIGHT + LABEL_BOT_OFFSET))
        self.other_cards_parent.set_parent(self.scroll_view.content)
        content_size_fitter = self.other_cards_parent.add_component(VerticalContentSizeFitter)
        content_size_fitter.after_space = 100

        layout_group = self.other_layouts_group = \
            self.other_cards_parent.add_component(GridLayoutGroup)
        layout_group.cell_size = Vector(200, 200 / 0.7)
        layout_group.spacing = 25

        # labels / titles
        label_deck = Text(position=Vector(0, 50),
                          size=Vector(self.screen_w, LABEL_HEIGHT),
                          title=translate_string('ui.own_deck'),
                          align='center',
                          valign='middle',
                          font_size=72)
        label_deck.set_parent(deck_background)

        label_other = Text(position=Vector(0, OWN_DECK_BOARD_HEIGHT + LABEL_BOT_OFFSET * 2),
                           size=Vector(self.screen_w, LABEL_HEIGHT),
                           title=translate_string('ui.others_cards'),
                           align='center',
                           valign='middle',
                           font_size=72)
        label_other.set_parent(deck_background)

        # swap cards
        self.swap_condidate = None

        self._displayed_nation = ''

    def displayed_nation(self):
        return self._displayed_nation

    def scroll_to_top(self):
        self.scroll_view.slider.set_value(0)

    def clear_scroll_view(self):
        for child in self.deck_cards_parent.get_children():
            child.set_parent(None)
            del child
        for child in self.other_cards_parent.get_children():
            child.set_parent(None)
            del child

    def display_nation(self, nation: str):
        self.clear_scroll_view()
        self.scroll_to_top()
        self._displayed_nation = nation

        self.display_deck(nation)
        self.display_other_cards(nation)

    def display_deck(self, nation: str):
        deck_cards = tuple(card_manager.deck_by_nation[nation])
        for card_info in deck_cards:
            card_obj = card_info.build_card_object()
            card_obj.add_component(CardClickHandler).init(card_info, self, True)
            card_obj.set_parent(self.deck_cards_parent)

        self.scroll_view.content.set_size(Vector(self.scroll_view.get_size().x,
                                                 self.deck_cards_parent.position.y +
                                                 self.deck_cards_parent.get_size().y - 50))

    def display_other_cards(self, nation: str):
        deck_cards = tuple(card_manager.deck_by_nation[nation])
        other_cards = tuple(set(card_manager.cards_by_nation[nation]) - set(deck_cards))
        for card_info in other_cards:
            card_obj = card_info.build_card_object()
            card_obj.add_component(CardClickHandler).init(card_info, self, False)
            card_obj.set_parent(self.other_cards_parent)

        self.scroll_view.content.set_size(Vector(self.scroll_view.get_size().x,
                                                 self.other_cards_parent.position.y +
                                                 self.other_cards_parent.get_size().y))

    def start_card_swap_operation(self):
        self.clear_scroll_view()
        self.scroll_to_top()
        self.display_deck(self._displayed_nation)
        self.nation_buttons.enabled = False
        self.card_swapping = True

    def swap_cards(self, in_deck, other):
        card_switcher.switch_cards(self._displayed_nation, in_deck, other)
        self.card_swapping = False
        self.display_nation(self._displayed_nation)
        self.nation_buttons.enabled = True

