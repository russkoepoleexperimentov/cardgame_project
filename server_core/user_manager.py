import json
import os.path
import random

ENCODING = 'utf-8'


def uniqueid():
    seed = random.getrandbits(32)
    while True:
        yield seed
        seed += 1


unique_sequence = uniqueid()


class UserManager:
    def __init__(self, working_dir):
        self._users = list()
        self.db_path = os.path.join(working_dir, 'data/players.json')

        self.load_db()

    def try_register_user(self, username, password):
        if len(tuple(filter(lambda x: x.username == username, self._users))):
            return False
        self._users.append(UserData(username, password))
        self.commit()
        return True

    def try_login(self, username, password):
        for user in self._users:
            if user.username == username:
                if user.password == password:
                    return True, user
                else:
                    return False, 'passwords did not match'

        return False, 'there are no users with this username'

    def load_db(self):
        if not os.path.exists(self.db_path):
            return

        with open(self.db_path, 'r', encoding=ENCODING) as file:
            users = json.load(file)
            for u in users:
                user = UserData(u['username'], u['password'], u['token'])
                user.chests = u['chests']
                self._users.append(user)

    def commit(self):
        users = []
        for u in self._users:
            users.append({
                'username': u.username,
                'password': u.password,
                'token': u.get_token(),
                'chests': u.chests,
            })
        with open(self.db_path, 'w', encoding=ENCODING) as file:
            json.dump(users, file, ensure_ascii=False, indent=2)

    def get_user_by_token(self, token: int):
        for u in self._users:
            if u.get_token() == token:
                return u


class UserData:
    def __init__(self, username, password, token=None):
        self.username = username
        self.password = password

        if token:
            self._token = token
        else:
            self._token = next(unique_sequence)

        self.chests = 10

    def get_token(self):
        return self._token
