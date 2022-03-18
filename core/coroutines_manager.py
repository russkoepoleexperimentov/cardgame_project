import asyncio
import signal
from asyncio import CancelledError

from core.log import trace

event_loop: asyncio.AbstractEventLoop = None


def init():
    trace('coroutines module: initializing')
    global event_loop
    event_loop = asyncio.get_event_loop()


def run_once():
    event_loop.call_soon(event_loop.stop)
    event_loop.run_forever()


def start_coroutine(routine):
    event_loop.create_task(routine)


def shut_down():
    trace('coroutines module: shutting down')

def get_event_loop():
    return event_loop
