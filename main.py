from core.application import Application
from core import scene_manager
from core import log
from scenes.menu import MenuScene

if __name__ == '__main__':
    log.start()
    app = Application('Hearts Of Iron V')
    scene_manager.load(MenuScene())
    app.run()
