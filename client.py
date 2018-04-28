import Pyro4
from remote import RemoteClient
import room

if __name__ == '__main__':
    with Pyro4.Daemon() as daemon:
        client = RemoteClient()
        client_uri = daemon.register(client)
        gameserver=Pyro4.Proxy('PYRONAME:example.pacmanserver')
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
            for ghost_uri in gameserver.start_room(room_name).ghosts:
                Pyro4.Proxy(ghost_uri).start()
            client.start()
            print('debug started')
        else:
            room = gameserver.connect_to_room(action, client_uri)

            for ghost_uri in room.ghosts:
                if ghost_uri != client_uri:
                    Pyro4.Proxy(ghost_uri).append_listener(client_uri)
                    client.append_listener(ghost_uri)
            client.append_listener(room.pacman_uri)

            print('Wait for the beginning.')
        daemon.requestLoop()
