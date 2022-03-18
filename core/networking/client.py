import asyncio
import socket
from pickle import loads, dumps

from core.coroutines_manager import start_coroutine, get_event_loop
from core import log
from server_core.server import SV_BUFFER_SIZE


class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self, server='127.0.0.1', port=5555):
        conn_task = self.connection_coroutine(server, port)
        start_coroutine(conn_task)

    async def connection_coroutine(self, server, port):
        loop = get_event_loop()
        try:
            await loop.sock_connect(self.socket, (server, port))
            self.connected = True
            start_coroutine(self.main_loop())
        except ConnectionRefusedError:
            log.trace('[CLIENT] server didn\'t responding...')
            self.connected = False

    async def main_loop(self, *args):
        if not self.connected:
            return
        loop = get_event_loop()
        data = await loop.sock_recv(self.socket, SV_BUFFER_SIZE)

        if bytearray(data):
            print('received data')
            self.receive_packet(data)

    def disconnect(self):
        if not self.connected:
            return

        self.connected = False
        self.socket.close()

    def send_packet(self, server: socket.socket, raw_data: tuple):
        data = dumps(raw_data)
        server.send(data)

    def receive_packet(self, raw_data: bytes):
        packet_name, *data = loads(raw_data)
        if packet_name == 'sv_full':
            log.trace('[CLIENT] server is full, disconnecting....')
            self.disconnect()
        if packet_name == 'sv_success':
            log.trace('[CLIENT] connection success, enjoy playing!')
