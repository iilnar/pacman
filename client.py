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
            room = gameserver.start_room(room_name)
            for uri in room.ghosts:
                Pyro4.Proxy(uri).start(room.ghosts + [client_uri])
            client.start(room.ghosts + [client_uri])
            print('debug started')
        else:
            room = gameserver.connect_to_room(action, client_uri)
            print('Wait for the beginning.')
        daemon.requestLoop()
