import Pyro4

# @Pyro4.expose
class Room(object):
    def __init__(self, room_name, pacman_uri):
        self._name = room_name
        self._pacmans_uri = [pacman_uri]
        self._started = False

    @property
    def name(self):
        return self._name

    @property
    def pacmans_uri(self):
        return self._pacmans_uri

    @property
    def started(self):
        return self._started

    def append_pacman(self, pacman_uri):
        self._pacmans_uri.append(pacman_uri)

    def start(self):
        self._started = True

def dict_to_room(cls, dct):
    ser = Pyro4.util.SerpentSerializer()
    room =  Room(dct['_name'], ser.recreate_classes(dct['_pacmans_uri'][0]))
    room._pacmans_uri.extend(ser.recreate_classes(dct['_pacmans_uri'][1:]))
    room._started = ser.recreate_classes(dct['_started'])
    return room

Pyro4.util.SerializerBase.register_dict_to_class('.'.join((Room.__module__, Room.__name__)), dict_to_room)
