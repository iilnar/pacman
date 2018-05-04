from tkinter import *
import Pyro4
from threading import Thread
import pacman
import random
import time


class MazeGrid(Canvas):
    def __init__(self, parent, width, height, square=15):
        self.width = width
        self.height = height
        self.square = square
        real_width = width * square
        real_height = height * square
        Canvas.__init__(self, parent, width = real_width, height = real_height, background='black')
        self.xview_moveto(0)
        self.yview_moveto(0)
        # self.create_line(square, 0 , square, real_height,width=2, fill='#001F77')
        # self.create_line(0, 0, 0, real_height, fill='#001F77')
        # self.create_line(0, y * square, real_width, y * square, fill='#001F77')
    def wall(self, x, y, color='#001F77'):
        x = x * self.square
        y = y * self.square
        self.create_rectangle(x, y, x + self.square, y + self.square, fill='black', outline=color,width=2)

class GUI(object):
    def __init__(self,width=25, height=20):
        Thread.__init__(self)
        self.tk = Tk()
        self.tk.wm_title("Pacman Distributed Game")
        self.maze_frame = Frame(self.tk, borderwidth=3, relief="raised", padx=2, pady=2, background='#946965')
        self.grid = MazeGrid(self.maze_frame, width, height, square=20)
        score_frame = Frame(self.tk, padx=2, pady=2)
        score_label = Label(score_frame, text="Players' score list:")
        score_label.pack(fill=X)
        self.listbox=Listbox(score_frame, width=15, height=20, font=(None,8))
        self.listbox.pack()

        self.createroombutton=Button(score_frame, text='Create room', command = lambda: self.buttonhandler.button_clicked('create_room'))
        self.createroombutton.pack()

        self.startgamebutton=Button(score_frame, text='Start game', command = lambda: self.buttonhandler.button_clicked('start_game'), state=DISABLED)
        self.startgamebutton.pack()

        self.joinroombutton=Button(score_frame, text='Join room', command = lambda: self.buttonhandler.button_clicked('join_room'))
        self.joinroombutton.pack()

        self.update_rooms=Button(score_frame, text='Update rooms', command = lambda: self.buttonhandler.button_clicked('update_rooms'))
        self.update_rooms.pack()

        self.maze_frame.bind('<Enter>', lambda x: self.maze_frame.focus_set())
        self.maze_frame.bind('<Key>', lambda event: print('pressed', repr(event.char)))

        self.statuslabel=Label(score_frame, width=20)
        self.statuslabel.pack(side=BOTTOM)
        self.grid.pack()
        self.maze_frame.pack(side=LEFT)
        score_frame.pack(side=RIGHT, fill=BOTH)
        self.buttonhandler  = None

    def enable_buttons(self, enabled=True):
        if enabled:
            self.startroombutton.config(state=NORMAL)
            self.joinroombutton.config(state=NORMAL)
            self.startgamebutton.config(state=NORMAL)
        else:
            self.startroombutton.config(state=DISABLED)
            self.joinroombutton.config(state=DISABLED)
            self.startgamebutton.config(state=DISABLED)

    def draw_creature(self, creature):
        x,y = creature.position
        x = x*self.grid.square
        y = y*self.grid.square
        tkid = self.grid.create_rectangle(x,y,x+self.grid.square,y+self.grid.square,fill=creature.color)
        return tkid

    def redraw_creature(self, creature):
        x,y =  creature.position
        x = x*self.grid.square
        y = y*self.grid.square
        self.grid.coords(creature.id, x, y, x+self.grid.square, y+self.grid.square)


    def run(self, game=None):
        if game:
            while self.game.in_progress:
                self.game.iteration()
                maze = self.game.maze.board
                ghosts = self.game.ghosts
                pacman = self.game.pacman
                # print("run", id(ghosts))
                # for ghost in ghosts:
                #     maze[ghost.position[0]][ghost.position[1]] = 'G'
                # maze[pacman.position[0]][pacman.position[1]] = 'P'
                self.redraw_creature(pacman)
                for ghost in ghosts:
                    self.redraw_creature(ghost)
                sleep(0.1)
            # stopit[0] = True
        else:
            return None

if __name__ == "__main__":
    width = 25
    height = 20
    gui = GUI(width,height)
    gui.grid.wall(3, 4)
    gui.grid.wall(3,5)
    gui.tk.mainloop()
