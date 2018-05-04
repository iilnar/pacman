import Pyro4

from threading import Thread
from utils import getch, clear
from game import Game
from creature import Creature

class Input(Thread):
    def __init__(self, creature, send_msg_all):
        Thread.__init__(self)
        self.creature = creature
        self.send_msg_all = send_msg_all

    def run(self):
        char = ''
        while char != 'q' and not stopit[0]:
            char = getch()
            _move_creature(self.creature, char)
            self.send_msg_all(char)
        stopit[0] = True


class Output(Thread):
    def __init__(self, game):
        Thread.__init__(self)
        self.game = game

    def run(self):
        cnt = 0
        while self.game.in_progress and not stopit[0]:
            cnt += 1
            clear()
            self.game.iteration()
            maze = self.game.maze.board
            ghosts = self.game.ghosts
            pacman = self.game.pacman
            # print("run", id(ghosts))
            for ghost in ghosts:
                maze[ghost.position[0]][ghost.position[1]] = 'G'
            maze[pacman.position[0]][pacman.position[1]] = 'P'
            for row in maze:
                print(''.join(row), end='\r\n')
        stopit[0] = True


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
        if idd == 0:
            _move_creature(self.game.pacman, char)
        else:
            _move_creature(_get_creature_by_id(self.game.pacmans, idd), char)

    def _keyboard_handler(self, event):
        _move_creature(self.creature, repr(event.char))
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

        for i, row in enumerate(self.game.maze.board):
            for j, chr in enumerate(row):
                if chr == '#':
                    self.gui.grid.wall(i, j)

        print('Started')
        for listener in self.listeners:
            with Pyro4.Proxy(listener) as obj:
                obj.send_msg(id(self), "hey, i miss you")
        print('Sent')
        out = Output(self.game)

        self.creature = _get_creature_by_id(self.game.pacmans, self.id)
