import argparse
import os.path
import random
import socket
import time
from _thread import start_new_thread
from pickle import loads, dumps

from server_core.server_resources import ServerResources
from server_core.user_manager import UserManager

SV_BUFFER_SIZE = 2048 * 4
SV_MAX_PLAYERS = 8

working_dir = os.path.dirname(os.path.abspath(__file__))


def uniqueid():
    seed = random.getrandbits(32)
    while True:
        yield seed
        seed += 1


unique_sequence = uniqueid()


class Server:
    def __init__(self, server='localhost', port=5555):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((server, port))
        self.socket.listen()
        self.connections = dict()

        self.resources = ServerResources(working_dir)
        self.user_manager = UserManager(working_dir)

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
                self.connections[uid] = connection_socket
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
        print('sending: ', raw_data)
        data = dumps(raw_data)
        client.send(data)

    def receive_packet(self, client, raw_data: bytes):
        packet_name, *data = loads(raw_data)
        if packet_name == 'authenticate_request':
            login_info = self.user_manager.try_login(*data)
            success, user_or_error = login_info

            if success:
                self.send_packet(client, ('authenticate_response', success,
                                          user_or_error.get_token()))
            else:
                self.send_packet(client, ('authenticate_response', success, user_or_error))
        if packet_name == 'register_request':
            registered = self.user_manager.try_register_user(*data)
            print(registered)
            self.send_packet(client, ('register_response', registered))


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--server', default='127.0.0.1:5555', type=str)
    args = arg_parser.parse_args()

    if args.server:
        try:
            print('[SERVER] Initializing')
            ip, port = map(lambda x: x.strip(), args.server.split(':'))
            server = Server(ip, int(port))
            server.start()
        except Exception as e:
            print(f'[SERVER] Something went wrong! \n\texception: {e}')
