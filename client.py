import Pyro4
import socket

from remote import RemoteClient
from threading import Thread
from game import Game
from pacman import Pacman
import room


class PyroClientThread(Thread):
    def __init__(self, daemon):
        Thread.__init__(self)
        self.setDaemon(False)
        self.daemon = daemon
    def run(self):
        daemon.requestLoop()
        print('finished loop')


def load_map(mapname='map.txt'):
    with open(mapname, 'r') as inp:
        n, m = map(int, inp.readline().split())
        mp = [list(inp.readline().strip()) for _ in range(n)]
        spawns = []
        for i, row in enumerate(mp):
            for j, c in enumerate(row):
                if c.isdigit():
                    spawns.append((i, j))
                    mp[i][j] = '.'
        return n, m, mp, spawns


if __name__ == '__main__':
    ip = socket.gethostbyname(socket.gethostname())
    with Pyro4.Daemon(ip) as daemon:
        client = RemoteClient()
        client_uri = daemon.register(client)
        PyroClientThread(daemon).start()

        gameserver = Pyro4.Proxy('PYRONAME:example.pacmanserver')
        print('Connected to gameserver.')
        print('To create new room type "+ room_name", otherwise enter room_id')
        rooms = gameserver.rooms
        for i, room_name in enumerate(rooms):
            print(i, room_name)
        action = input()
        room = None
        if action.startswith('+'):
            _, room_name = action.split(maxsplit=1)
            room = gameserver.new_room(room_name, client_uri)
            print('Wait for other players, then type "start".')
            action = input()
            while action != 'start':
                action = input()
                game = Game()
            print('debug starting')
            room = gameserver.start_room(room_name)
            ghosts_count = len(room.ghosts)
            height, width, mp, spawns = load_map()
            params = {
                "width": width,
                "height": height,
                "map": mp,
                "pacman": (0, spawns[0]),
                "ghosts": [(i, point) for (i, point)  in enumerate(spawns[1:ghosts_count+1], 1)]
            }
            counter = 1
            for ghost_client_uri in room.ghosts:
                with Pyro4.Proxy(ghost_client_uri) as ghost_client:
                    ghost_client.start(game_params=params, id=counter)
                    counter += 1
            client.start(game_params=params, id=0)
            print('debug started')
            daemon.requestLoop()
        else:
            room = gameserver.connect_to_room(action, client_uri)
            for ghost_client_uri in room.ghosts:
                if ghost_client_uri != client_uri:
                    with Pyro4.Proxy(ghost_client_uri) as ghost_client:
                        ghost_client.append_listener(client_uri)
                        client.append_listener(ghost_client_uri)
            with Pyro4.Proxy(room.pacman_uri) as pacman_client:
                pacman_client.append_listener(client_uri)
                client.append_listener(room.pacman_uri)
            print('Wait for the game start')
            daemon.requestLoop()
            while True:
                pass
