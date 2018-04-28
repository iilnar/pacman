import Pyro4

from threading import Thread
from utils import getch, clear
from game import Game
from creature import Creature


class Input(Thread):
    def __init__(self, creature):
        Thread.__init__(self)
        self.creature = creature

    def run(self):
        char = ''
        while char != 'q':
            char = getch()
            self.creature.move(char)


class Output(Thread):
    def __init__(self, game):
        Thread.__init__(self)
        self.maze = maze

    def run(self):
        for _ in range(1000):
            clear()
            print(str(self.game.maze()).replace('\n', '\r\n'), end='\r\n')


@Pyro4.expose
class RemoteClient(object):
    def __init__(self):
        self.x, self.y = 0, 0
        self.listeners = []

    def change_direction(self, direction):
        print(direction)
        self.x, self.y = direction

    def send_msg(self, frm, msg):
        print("msg to:", id(self))
        print("msg from:", frm)
        print("msg msg:", msg)

    def append_listener(self, listener_uri):
        self.listeners.append(listener_uri)

    def start(self, *args, **kwargs):
        game = Game
        print('Started')
        for listener in self.listeners:
            with Pyro4.Proxy(listener) as obj:
                obj.send_msg(id(self), "hey, i miss you")
        print('Sent')
