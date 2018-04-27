from utils import getch, clear
from threading import Thread
from game import Game


class Input(Thread):
    def __init__(self, func):
        Thread.__init__(self)
        self.handler = func

    def run(self):
        char = ''
        while char != 'q':
            char = getch()
            self.handler(char)


class Output(Thread):
    def __init__(self, maze):
        Thread.__init__(self)
        self.maze = maze

    def run(self):
        for _ in range(1000):
            clear()
            print(str(self.maze()).replace('\n', '\r\n'), end='\r\n')


if __name__ == '__main__':
    z = Game()
    inp = Input(lambda c: z.move(c))
    out = Output(lambda: z.get())
    out.start()
    inp.start()

    # maze = Maze(5, 5)
    # for _ in range(5):
    #     clear()
    #     print maze
    #     # char = getch()
    #     # print (char,)
