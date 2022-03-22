from multiprocessing import Process

from core.application import Application
from core import application
from core.localization import load_localization, translate_string
from core import scene_manager
from core import log
from scenes.menu import MenuScene

from game import player_data_manager
from game.cards import card_manager

import argparse

from scenes.startup_scene import StartupScene
from server_core.server import Server

if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--server', type=str)
    arg_parser.add_argument('--client', default='127.0.0.1:5555', type=str)
    arg_parser.add_argument('--login', default='', type=str)
    args = arg_parser.parse_args()

    player_data_manager.init()
    load_localization('languages/russian.csv')
    log.start()
    app = Application(translate_string('game_name'))

    if args.server:
        try:
            print('[SERVER] Initializing')
            ip, port = map(lambda x: x.strip(), args.server.split(':'))
            server = Server(ip, int(port))
            server.start()
        except Exception as e:
            print(f'[SERVER] Something went wrong! \n\texception: {e}')

    if args.client:
        try:
            log.trace('[CLIENT] Initializing client')
            ip, port = map(lambda x: x.strip(), args.client.split(':'))
            application.client.connect(ip, int(port))
        except Exception as e:
            log.trace(f'[CLIENT] Something went wrong! \n\texception: {e}')

    username, password = '', ''
    if args.login:
        try:
            username, password = map(lambda x: x.strip(), args.login.split())
        except:
            pass

    # card_manager.init()
    scene_manager.load(StartupScene(username, password))
    app.run()
