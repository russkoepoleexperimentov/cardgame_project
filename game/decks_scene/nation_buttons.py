from core.component import Component
from core.localization import translate_string
from core.ui.button import Button
from core.ui.image import Image
from core.ui.layout_group import HorizontalLayoutGroup
from core.vector import Vector
from game.button_sounds import ButtonSounds
from game.cards import card_manager
from game.contstants import BUTTON_DEFAULT_DESIGN


# buttons
from game.decks_scene.cards_list import CardsList

BTN_SIZE = Vector(150, 30)
BTN_MARGIN = 5


class NationButtons(Component):
    def __init__(self, owner: Image):
        super(NationButtons, self).__init__(owner)

        self.cards_list: CardsList = None

        horizontal_layout_group = owner.add_component(HorizontalLayoutGroup)
        horizontal_layout_group.spacing = BTN_MARGIN

        nations = sorted(card_manager.nations)

        self.nation_buttons = dict()

        for nation in nations:
            btn = Button(**BUTTON_DEFAULT_DESIGN, size=BTN_SIZE, title=translate_string(nation))
            btn.set_parent(owner)
            btn.add_component(ButtonSounds)
            btn.label.set_font_size(20)
            btn.on_click.add_listener(lambda name=nation: self.display_nation(name))
            self.nation_buttons[nation] = btn

    def set_cards_list(self, cards_list):
        self.cards_list = cards_list
        nations = sorted(card_manager.nations)

        if nations:
            self.display_nation(nations[0])

    def display_nation(self, nation: str):
        for button in self.nation_buttons.values():
            button.interactable = True
        self.nation_buttons[nation].interactable = False

        self.cards_list.display_nation(nation)
