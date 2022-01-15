from core.component import Component
from card_info import CardInfo


class GameCard(Component, CardInfo):
    def __init__(self, owner, ):
        super(Component).__init__(owner)

    def card_info(self, name):
        super(CardInfo).__init__(name)