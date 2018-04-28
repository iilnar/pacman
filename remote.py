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
        while char != 'q':
            char = getch()
            self.creature.move(char)
            self.send_msg_all(char)


class Output(Thread):
    def __init__(self, game):
        Thread.__init__(self)
        self.game = game

    def run(self):
        for _ in range(1):
            clear()
            maze = self.game.maze.board
            ghosts = self.game.ghosts
            pacman = self.game.pacman
            for ghost in ghosts:
                maze[ghost.position[0]][ghost.position[1]] = 'G'
            maze[pacman.position[0]][pacman.position[1]] = 'P'
            for row in maze:
                print(''.join(row), end='\r\n')


@Pyro4.expose
class RemoteClient(object):
    def __init__(self):
        self.x, self.y = 0, 0
        self.listeners = []
        self.game = None

    def change_direction(self, direction):
        print(direction)
        self.x, self.y = direction

    def send_msg(self, frm, msg):
        print("msg to:", id(self))
        print("msg from:", frm)
        print("msg msg:", msg)

    def make_move(self, idd, char):
        def move_creature(creat, chr):
            if chr == 'w':
                creat.move_up()
            elif chr == 'd':
                creat.move_right()
            elif chr == 's':
                creat.move_down()
            elif chr == 'a':
                creat.move_left()

        if idd == 0:
            move_creature(self.game.pacman, char)
        else:
            for ghost in self.ghosts:

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
        print('Started')
        for listener in self.listeners:
            with Pyro4.Proxy(listener) as obj:
                obj.send_msg(id(self), "hey, i miss you")
        print('Sent')
        out = Output(self.game)
        out.start()
