import Pyro4
from remote import RemoteClient
from threading import Thread
import room


class PyroClientThread(Thread):
    def __init__(self, daemon):
        Thread.__init__(self)
        self.setDaemon(False)
        self.daemon = daemon
    def run(self):
        daemon.requestLoop()
        print('finished loop')

if __name__ == '__main__':
    with Pyro4.Daemon() as daemon:
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
            print('debug starting')
            room = gameserver.start_room(room_name)
            for ghost_client_uri in room.ghosts:
                with Pyro4.Proxy(ghost_client_uri) as ghost_client:
                    ghost_client.start()
            client.start()
            print('debug started')
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
                while True:
                    pass
