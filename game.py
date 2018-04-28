from maze import Maze
from pacman import Pacman
from ghost import Ghost

class Game:
    def __init__(self, game_params):
        width = game_params["width"]
        height = game_params["height"]
        ghosts = game_params["ghosts"]
        pacman = game_params["pacman"][1]
        mp = game_params['map']

        self._pacman = Pacman(pacman)
        self._ghosts = [Ghost(ghost[1]) for ghost in ghosts]
        self._maze = Maze(mp)

    @property
    def pacman(self):
        return self._pacman

    @property
    def ghosts(self):
        return self._ghosts

    @property
    def maze(self):
        return self._maze

    def move(self, chr):
        pass
        # if not self.maze.is_wall(self.pacman.get_move()):
        #     self.pacman.move()
        #     self.maze.set_pacman(self.pacman.pos)

    def to_params(self):
        spawns = self._maze.spawn_points
        width, height = self._maze.get_dimensions
        ghosts_count = self._ghosts.length + 1
        return {
            "width": width,
            "height": height,
            "pacman": (0, spawns[0]),
            "ghosts": [(i, point) for (i, point)  in zip(range(1, ghosts_count), spawns[1:ghosts_count])]

        }

    def get(self):
        return self._maze

    def connect_ghost(self, ghost):
        self._ghosts.append(ghost)
