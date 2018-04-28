from maze import Maze
from pacman import Pacman


class Game:
    def __init__(self, **game_params):
        width = game_params["width"]
        height = game_params["height"] 
        ghosts  game_params["ghostts"]
        pacman = game_params["pacman"][1]
        self.arr = []
        if game_params:
            self.pacman = Pacman(pacman)
            self.ghosts = [Ghost(ghost[1]) for ghost in ghosts]
            self.maze = Maze(width, length, pacman)
        else:
            self.pacman = Pacman(1, 1)
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
    
    def to_params(self):
        spawns = self.maze.spawn_points
        width, height = self.maze.get_dimensions
        ghosts_count = self.ghosts.length + 1
        return {
            "width": width,
            "height": height,
            "pacman": (0, spawns[0]),
            "ghosts": [(i, point) for (i, point)  in zip(range(1, ghosts_count), spawns[1:ghosts_count])]
            
        }

    def get(self):
        return self.maze


    def connect_ghost(self, ghost):
        self.ghosts.append(ghost)


