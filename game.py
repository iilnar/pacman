from maze import Maze
from pacman import Pacman


class Game:
    def __init__(self):
        self.arr = []
        self.pacman = Pacman((1, 1))
        self.ghosts = [Ghost(2, 2), Ghost(3, 3)]
        self.maze = Maze(5, 5, self.pacman.pos)

    def move(self, chr):
        if chr == 'w':
            self.pacman.move_up()
        elif chr == 'd':
            self.pacman.move_right()
        elif chr == 's':
            self.pacman.move_down()
        elif chr == 'a':
            self.pacman.move_left()

        if not self.maze.is_wall(self.pacman.get_move()):
            self.pacman.move()
            self.maze.set_pacman(self.pacman.pos)

    def get(self):
        return self.maze
