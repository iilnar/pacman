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

        self._in_progress = True
        self._pacman = Pacman(0, pacman)
        self._ghosts = [Ghost(ghost[0], ghost[1]) for ghost in ghosts]
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

    @property
    def in_progress(self):
        return self._in_progress

    def move(self, creat):
        if not self.maze.is_wall(creat.get_move()):
            creat.move()

    def iteration(self):
        self.move(self.pacman)
        for ghost in self.ghosts:
            self.move(ghost)
        if self.maze.has_coin(self.pacman.position):
            self.pacman.inc_score()
            self.maze.remove_coin(self.pacman.position)
        for ghost in self.ghosts:
            if ghost.position == self.pacman.position:
                self._in_progress = False

    def to_params(self):
        spawns = self._maze.spawn_points
        width, height = self._maze.get_dimensions
        ghosts_count = self._ghosts.length
        return {
            "width": width,
            "height": height,
            "pacman": (0, spawns[0]),
            "ghosts": [(i, point) for (i, point) in enumerate(spawns[1:ghosts_count+1], 1)]
        }

    def get(self):
        return self._maze

    def connect_ghost(self, ghost):
        self._ghosts.append(ghost)
