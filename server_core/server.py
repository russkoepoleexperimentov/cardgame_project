import argparse
import socket
import time
from _thread import start_new_thread
from pickle import loads, dumps

SV_BUFFER_SIZE = 2048


class Server:
    def __init__(self, server='localhost', port=5555):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((server, port))
        self.socket.listen()

    def start(self):
        print('[SERVER] Starting')
        self.connections = 0
        print('[SERVER] Waiting for connections')
        start_new_thread(self.receive_connections, tuple())


    def receive_connections(self):
        while True:
            connection_socket, address = self.socket.accept()
            print('conn', self.connections)
            if self.connections > 2:
                self.send_packet(connection_socket, ('sv_full',))
            else:
                self.send_packet(connection_socket, ('sv_success',))
                self.connections += 1
                start_new_thread(self.client_thread, (connection_socket,))
            time.sleep(0.1)

    def client_thread(self, client):
        while True:
            try:
                raw_data = client.recv(SV_BUFFER_SIZE)

                if not raw_data:
                    break

                self.receive_packet(raw_data)
            except:
                pass

        self.connections -= 1

    def send_packet(self, client: socket.socket, raw_data: tuple):
        data = dumps(raw_data)
        client.send(data)

    def receive_packet(self, raw_data: bytes):
        packet_name, *data = loads(raw_data)
        if packet_name == 'authenticate_uid':
            self.send_packet()


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
