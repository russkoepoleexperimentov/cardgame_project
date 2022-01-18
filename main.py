from core.application import Application
from core.localization import load_localization, translate_string
from core import scene_manager
from core import log
from scenes.menu import MenuScene

from game.cards import card_manager

if __name__ == '__main__':
    load_localization('languages/russian.csv')
    log.start()
    app = Application(translate_string('game_name'))
    card_manager.init()
    scene_manager.load(MenuScene())
    app.run()
