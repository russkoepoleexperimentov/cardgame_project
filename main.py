from core.game import Game
from core import scene_manager
from scenes.menu import MenuScene

if __name__ == '__main__':
    app = Game('Hearts Of Iron V')
    scene_manager.load(MenuScene())
    app.run()
