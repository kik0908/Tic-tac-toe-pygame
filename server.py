import asyncio
import random
from string import ascii_uppercase, digits


def generate_id(lenght=6):
    abc = ascii_uppercase + digits
    return ''.join(random.sample(abc, lenght))


class GameManager:
    def __init__(self):
        self.games = {}

        self.free_games = []
        self.free_games_num = 0
        self.not_free_games = []

    def _create_new_game(self):
        _id = generate_id()

        self.free_games.append(_id)
        self.free_games_num += 1

        self.games[_id] = Game(_id)

    def get_free_game(self):
        if self.free_games_num > 0:
            _game: Game = self.free_games.pop(0)
            self.free_games_num -= 1
            self.not_free_games.append(self.games[_game].id)
            return _game
        else:
            self._create_new_game()
            return self.get_free_game()

    def get_game(self, id):
        return self.games[id]


class Game:
    def __init__(self, id):
        self.id = id
        self.player = 0
        self.players = []

    def add_player(self):
        pass

    @property
    def active_symbol(self):
        return 'x' if self.player == 1 else 'o'

    def swap_symbol(self):
        self.player = not self.player


class Commands:
    @staticmethod
    def get_game():
        return game_manager.get_free_game()

    @staticmethod
    def get_active_symbol(game_id):
        return game_manager.get_game(game_id).active_symbol

    @staticmethod
    def swap_symbol(game_id):
        game_manager.get_game(game_id).swap_symbol()
        return 0


commands = {'get_game': Commands.get_game,
            'get_active_symbol': Commands.get_active_symbol,
            'swap_symbol': Commands.swap_symbol}

a = 0


async def ab():
    while True:
        await asyncio.sleep(1)
        print(a)


async def handle_echo(reader, writer):
    while True:
        data = await reader.read(1024)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        print(f"Received {message!r} from {addr!r}")

        if data == '' or writer.is_closing():
            break

        print(f"Send: {message!r}")
        writer.write(data)
        await writer.drain()

    print("Close the connection")
    writer.close()


async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


game_manager = GameManager()
asyncio.run(main())
