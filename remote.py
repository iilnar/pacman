import Pyro4

from threading import Thread
from utils import getch, clear
from game import Game
from creature import Creature


def _get_creature_by_id(ls, idd):
    for pacman in ls:
        if idd == idd:
            return pacman
    return None


def _move_creature(creat, chr):
    if chr == 'w':
        creat.move_up()
    elif chr == 'd':
        creat.move_right()
    elif chr == 's':
        creat.move_down()
    elif chr == 'a':
        creat.move_left()


@Pyro4.expose
class RemoteClient(object):
    def __init__(self, gui):
        self.x, self.y = 0, 0
        self.listeners = []
        self.game = None
        self.gui = gui

    def change_direction(self, direction):
        print(direction)
        self.x, self.y = direction

    def send_msg(self, frm, msg):
        print("msg to:", id(self))
        print("msg from:", frm)
        print("msg msg:", msg)

    def make_move(self, idd, char):
        _move_creature(_get_creature_by_id(self.game.pacmans, idd), char)

    def _keyboard_handler(self, event):
        print(event)
        _move_creature(self.creature, event.char)
        self.send_msg_all(repr(event.char))

    def send_msg_all(self, char):
        for listener in self.listeners:
            with Pyro4.Proxy(listener) as obj:
                obj.make_move(self.id, char)

    def append_listener(self, listener_uri):
        self.listeners.append(listener_uri)

    def start(self, **kwargs):
        game_params = kwargs['game_params']
        self.id = kwargs['id']
        self.game = Game(game_params=game_params)
        self.gui.keyboardhandler = lambda event: self._keyboard_handler(event)
        self.game.coin2tkid = {}

        for i, row in enumerate(self.game.maze.board):
            for j, chr in enumerate(row):
                if chr == '#':
                    self.gui.grid.wall(i, j)
                elif chr == '.':
                    self.game.coin2tkid[(i, j)] = self.gui.grid.coin(i, j)

        self.creature = _get_creature_by_id(self.game.pacmans, self.id)

        class TThread(Thread):
            def __init__(self, gui, game):
                Thread.__init__(self)
                self.gui = gui
                self.game = game

            def run(self):
                self.gui.run(self.game)
        TThread(self.gui, self.game).start()

        print('Started')
        for listener in self.listeners:
            with Pyro4.Proxy(listener) as obj:
                obj.send_msg(id(self), "hey, i miss you")
