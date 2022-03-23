import argparse
import os.path
import random
import socket
import time
from _thread import start_new_thread
from pickle import loads, dumps
from zlib import compress, decompress

if __name__ == '__main__':
    from server_resources import ServerResources
    from user_manager import UserManager
    from lobby import Lobby
else:
    from server_core.server_resources import ServerResources
    from server_core.user_manager import UserManager
    from server_core.lobby import Lobby

SV_BUFFER_SIZE = 2048 * 4
SV_MAX_PLAYERS = 8

working_dir = os.path.dirname(os.path.abspath(__file__))


def uniqueid():
    seed = random.getrandbits(32)
    while True:
        yield seed
        seed += 1


unique_sequence = uniqueid()
global_server = None


class Server:
    def __init__(self, server='localhost', port=5555):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((server, port))
        self.socket.listen()
        self.connections = dict()

        self.resources = ServerResources(working_dir)
        self.user_manager = UserManager(working_dir)

        self.lobbies = dict()

        global global_server
        global_server = self

    def start(self):
        print('[SERVER] Starting')
        self.connections = dict()
        print('[SERVER] Waiting for connections')
        start_new_thread(self.receive_connections, tuple())

    def receive_connections(self):
        while True:
            connection_socket, address = self.socket.accept()
            if len(self.connections) > SV_MAX_PLAYERS:
                self.send_packet(connection_socket, ('sv_full',))
            else:
                uid = next(unique_sequence)
                self.connections[uid] = [connection_socket]
                print(self.connections)
                print(connection_socket)
                self.send_packet(connection_socket, ('sv_success', uid))
                start_new_thread(self.client_thread, (connection_socket, uid))
            time.sleep(0.1)

    def client_thread(self, client, client_uid):
        while True:
            try:
                raw_data = client.recv(SV_BUFFER_SIZE)

                if not raw_data:
                    break

                self.receive_packet(client, raw_data)
            except:
                pass

        del self.connections[client_uid]

    def send_packet(self, client: socket.socket, raw_data: tuple):
        data = dumps(raw_data)
        compressed_data = compress(data)
        client.send(compressed_data)

    def receive_packet(self, client, raw_data: bytes):
        packet_name, token, *data = loads(decompress(raw_data))
        user = self.user_manager.get_user_by_token(token)
        if packet_name == 'authenticate_request':
            login_info = self.user_manager.try_login(*data)
            success, user_or_error = login_info

            if success:
                self.connections[self.uid(client)].append(user_or_error)
                self.send_packet(client, ('authenticate_response', success,
                                          user_or_error.get_token()))
            else:
                self.send_packet(client, ('authenticate_response', success, user_or_error))
        if packet_name == 'register_request':
            registered = self.user_manager.try_register_user(*data)
            self.send_packet(client, ('register_response', registered))
        if packet_name == 'get_user_cards':
            pass
        if packet_name == 'get_chests_count':
            self.send_packet(client, ('chests_count_response',
                                      self.user_manager.get_user_by_token(token).chests))
        if packet_name == 'open_chest':
            if user.chests < 1:
                self.send_packet(client, ('open_chest_response', ''))
            else:
                user.chests -= 1
                closed_cards = tuple(set(self.resources.card_sections()) - set(user.unlocked_cards))
                card = random.choice(closed_cards)
                user.unlocked_cards.append(card)
                self.user_manager.commit()
                self.send_packet(client, ('open_chest_response', card))
        if packet_name == 'get_all_cards':
            self.send_packet(client, ('all_cards_response', self.resources.cards_tuple()))
        if packet_name == 'get_decks':
            nations = self.resources.nations()
            decks = dict()
            for n in nations:
                decks.update({n: tuple(user.decks.get(n, []))})
            self.send_packet(client, ('decks_response', decks))
        if packet_name == 'get_unlocked_cards':
            self.send_packet(client, ('unlocked_cards_response', tuple(user.unlocked_cards)))
        if packet_name == 'switch_deck_card':
            card_not_in_deck, card_in_deck, nation = data
            card_not_in_deck, card_in_deck = (self.resources.card_by_section(card_not_in_deck),
                                              self.resources.card_by_section(card_in_deck))
            if card_not_in_deck.nation == nation and card_in_deck.nation == nation:
                user.decks[nation].append(card_not_in_deck.section)
                user.decks[nation].remove(card_in_deck.section)
                self.user_manager.commit()
        if packet_name == 'create_lobby':
            lobby = Lobby()
            self.lobbies.update({lobby.id: lobby})
            self.send_packet(client, ('create_lobby_response', lobby.id))
        if packet_name == 'join_lobby':
            lobby_id = data[0]
            err = ''
            try:
                lobby = self.lobbies[lobby_id]
                for u in lobby.players:
                    if u is not user:
                        self.send_packet(self.connections[self.uid(u)][0], ('player_join',))
                lobby.players.append(user)
            except:
                err = f'lobby with id {lobby_id} not found'
            self.send_packet(client, ('join_lobby_response', err, lobby_id))
        if packet_name == 'leave_lobby':
            lobby_id = data[0]
            try:
                lobby = self.lobbies[lobby_id]
                for u in lobby.players:
                    if u is not user:
                        self.send_packet(self.connections[self.uid(u)][0], ('player_left',))

                lobby.players.remove(user)
            except:
                pass
        if packet_name == 'ready':
            lobby_id = data[0]


    def uid(self, thing):
        for k in self.connections:
            if thing in self.connections[k]:
                return k

server = None
if __name__ == '__main__':
    from time import sleep

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--server', default='127.0.0.1:5555', type=str)
    args = arg_parser.parse_args()

    if args.server:
        try:
            print('[SERVER] Initializing')
            ip, port = map(lambda x: x.strip(), args.server.split(':'))
            server = Server(ip, int(port))
            server.start()
            while True:
                try:
                    sleep(1)
                except KeyboardInterrupt:
                    print('[SERVER] Shutting down')
                    exit(0)
        except Exception as e:
            print(f'[SERVER] Something went wrong! \n\texception: {e}')
