import random

def uniqueid():
    seed = random.getrandbits(32)
    while True:
        yield seed
        seed += 1


unique_sequence = uniqueid()


class Lobby:
    def __init__(self):
        self.players = []
        self.ready_players = 0
        self.id = next(unique_sequence)

