import Pyro4

# @Pyro4.expose
class Room(object):
    def __init__(self, room_name, pacman_uri):
        self._name = room_name
        self._pacman_uri = pacman_uri
        self._ghosts = []
        self._started = False

    @property
    def name(self):
        return self._name

    @property
    def pacman_uri(self):
        return self._pacman_uri

    @property
    def ghosts(self):
        return self._ghosts

    @property
    def started(self):
        return self._started

    def append_ghost(self, ghost):
        self.ghosts.append(ghost)

    def start(self):
        self._started = True


def dict_to_room(cls, dct):
    ser = Pyro4.util.SerpentSerializer()
    room =  Room(dct['_name'], ser.recreate_classes(dct['_pacman_uri']))
    room._ghosts = ser.recreate_classes(dct['_ghosts'])
    room._started = ser.recreate_classes(dct['_started'])
    return room

Pyro4.util.SerializerBase.register_dict_to_class('.'.join((Room.__module__, Room.__name__)), dict_to_room)
