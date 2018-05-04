import Pyro4
import socket
from threading import Thread
from remote import RemoteClient
from room import Room


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class GameServer(object):
    def __init__(self):
        self._rooms = {}

    @property
    def rooms(self):
        return self._rooms.keys()

    def new_room(self, room_name, client_uri):
        print("new room from", client_uri)
        room = Room(room_name, client_uri)
        # self._pyroDaemon.register(room)
        self._rooms[room_name] = room

        print("rooms count:", len(self._rooms))
        return room

    def connect_to_room(self, room_name, client_uri):
        if not self._rooms[room_name].started:
            self._rooms[room_name].append_pacman(client_uri)
            return self._rooms[room_name]

    def start_room(self, room_name):
        self._rooms[room_name].start()
        return self._rooms[room_name]


class PyroDaemonThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.pyroserver = GameServer()
        ip = socket.gethostbyname(socket.gethostname())
        self.pyrodaemon=Pyro4.Daemon(ip)
        self.ns=Pyro4.locateNS()
        self.setDaemon(False)
    def run(self):
        with self.pyrodaemon:
            with self.ns:
                uri=self.pyrodaemon.register(self.pyroserver)
                self.ns.register("example.pacmanserver", uri)
                print("Pyro server registered on %s" % self.pyrodaemon.locationStr)
                self.pyrodaemon.requestLoop()


if __name__ == '__main__':
    try:
        PyroDaemonThread().start()
    except Pyro4.errors.NamingError:
        print("Can't find the Pyro Nameserver. Running without remote connections.")
