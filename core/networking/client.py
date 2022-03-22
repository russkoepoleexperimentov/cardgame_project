import asyncio
import socket
from zlib import compress, decompress
from pickle import loads, dumps

from core.action import Action
from core.coroutines_manager import start_coroutine, get_event_loop
from core import log
from server_core.server import SV_BUFFER_SIZE

from server_core.server_resources import CardInfo


class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected_stage = 0
        self.token = ''
        self.authenticated = False
        self.on_packet = Action()
        self.uid = ''

        self.username = ''
        self.password = ''

    def authenticate(self, username, password):
        self.username = username
        self.password = password
        self.authenticated = False
        start_coroutine(self.authenticate_coroutine())

    async def authenticate_coroutine(self):
        while not self.connected_stage == 2:
            await asyncio.sleep(0)

        log.trace('[CLIENT] trying to authenticate...')
        self.send_packet(('authenticate_request', self.username, self.password))

    def register(self, username, password):
        self.username = username
        self.password = password
        start_coroutine(self.register_coroutine())

    async def register_coroutine(self):
        while not self.connected_stage == 2:
            await asyncio.sleep(0)

        log.trace('[CLIENT] trying to register...')
        self.send_packet(('register_request', self.username, self.password))

    def connect(self, server='127.0.0.1', port=5555):
        conn_task = self.connection_coroutine(server, port)
        start_coroutine(conn_task)

    async def connection_coroutine(self, server, port):
        loop = get_event_loop()
        try:
            await loop.sock_connect(self.socket, (server, port))
            self.connected_stage = 1
            start_coroutine(self.main_loop())
        except ConnectionRefusedError:
            log.trace('[CLIENT] server didn\'t responding...')
            self.on_packet.invoke('sv_connrefused')
            self.connected_stage = 0

    async def main_loop(self, *args):
        if not self.connected_stage:
            return
        loop = get_event_loop()

        while True:
            try:
                data = await loop.sock_recv(self.socket, SV_BUFFER_SIZE)
                self.receive_packet(data)
            except Exception as e:
                print(e)

    def disconnect(self):
        if not self.connected_stage:
            return

        self.connected_stage = 0
        self.authenticated = False
        self.uid = ''
        self.socket.close()

    def send_packet(self, raw_data: tuple):
        raw_data = list(raw_data)
        raw_data.insert(1, self.token)
        data = dumps(raw_data)
        compressed_data = compress(data)
        self.socket.send(compressed_data)

    def receive_packet(self, raw_data: bytes):
        packet_name, *data = loads(decompress(raw_data))
        self.on_packet.invoke(packet_name, *data)
        if packet_name == 'sv_full':
            log.trace('[CLIENT] server is full, disconnecting....')
            self.disconnect()
        if packet_name == 'sv_success':
            log.trace('[CLIENT] connection success, uid is ' + str(data[0]))
            self.uid = data[0]
            self.connected_stage = 2
        if packet_name == 'authenticate_response':
            if data[0] is True:
                self.token = data[1]
                self.authenticated = True
                log.trace('[CLIENT] authentication success!')
            else:
                log.trace('[CLIENT] authentication fail: ' + data[1])
        if packet_name == 'register_response':
            if data[0] is True:
                log.trace('[CLIENT] register success!')
            else:
                log.trace('[CLIENT] register failed.')
