import Pyro4
import socket

from remote import RemoteClient
from threading import Thread
from game import Game
from pacman import Pacman
from gui import GUI
from tkinter import END, NORMAL
import room


class PyroClientThread(Thread):
    def __init__(self, daemon):
        Thread.__init__(self)
        self.setDaemon(False)
        self.daemon = daemon
    def run(self):
        while True:
            daemon.requestLoop()
        print('finished loop')


def load_map(mapname='map.txt'):
    with open(mapname, 'r') as inp:
        n, m = map(int, inp.readline().split())
        mp = [list(inp.readline().strip()) for _ in range(n)]
        spawns = []
        for i, row in enumerate(mp):
            for j, c in enumerate(row):
                if c.isdigit():
                    spawns.append((i, j))
                    mp[i][j] = '.'
        return n, m, mp, spawns

class ButtonHandler:
    def __init__(self):
        self.handlers = {}

    def assign_handler(self, button_name, handler):
        self.handlers[button_name] = handler

    def button_clicked(self, name):
        print(name)
        if name in self.handlers:
            self.handlers[name]()


if __name__ == '__main__':
    gui = GUI()

    gui.buttonhandler = ButtonHandler()

    ip = socket.gethostbyname(socket.gethostname())
    daemon = Pyro4.Daemon(ip)

    client = RemoteClient()
    client_uri = daemon.register(client)
    PyroClientThread(daemon).start()

    gameserver = Pyro4.Proxy('PYRONAME:example.pacmanserver')
    print('Connected to gameserver.')

    def new_room():
        gameserver.new_room(ip, client_uri)
        update_rooms()
        gui.startgamebutton.config(state=NORMAL)

    gui.buttonhandler.assign_handler('create_room', new_room)

    def start_game():
        room_name = ip
        room = gameserver.start_room(room_name)
        ghosts_count = len(room.ghosts)
        height, width, mp, spawns = load_map()
        params = {
            "width": width,
            "height": height,
            "map": mp,
            "pacman": (0, spawns[0]),
            "ghosts": [(i, point) for (i, point)  in enumerate(spawns[1:ghosts_count+1], 1)]
        }
        counter = 1
        for ghost_client_uri in room.ghosts:
            with Pyro4.Proxy(ghost_client_uri) as ghost_client:
                ghost_client.start(game_params=params, id=counter)
                counter += 1
        client.start(game_params=params, id=0)

    gui.buttonhandler.assign_handler('start_game', start_game)

    def update_rooms():
        rooms = gameserver.rooms
        gui.listbox.delete(0, END)
        for room_name in rooms:
            gui.listbox.insert(END, room_name)

    gui.buttonhandler.assign_handler('update_rooms', update_rooms)

    def join_room():
        if gui.listbox.curselection():
            room_name = gui.listbox.get(gui.listbox.curselection()[0])
            print('connecting to', room_name)
            room = gameserver.connect_to_room(room_name, client_uri)
            for ghost_client_uri in room.ghosts:
                if ghost_client_uri != client_uri:
                    with Pyro4.Proxy(ghost_client_uri) as ghost_client:
                        ghost_client.append_listener(client_uri)
                        client.append_listener(ghost_client_uri)
            with Pyro4.Proxy(room.pacman_uri) as pacman_client:
                pacman_client.append_listener(client_uri)
                client.append_listener(room.pacman_uri)
            print('connected')

    gui.buttonhandler.assign_handler('join_room', join_room)

    # gui.maze_frame.bind('<Button-1>', lambda x: gui.maze_frame.focus_set())
    # gui.maze_frame.bind('<Key>', lambda x: print('pressed', x))
    # gui.bind('<Key>', lambda x: print('pressed', x))

    gui.tk.mainloop()
