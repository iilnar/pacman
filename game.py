from maze import Maze
from pacman import Pacman


class Game:
    def __init__(self, game_params):
        width = game_params["width"]
        height = game_params["height"]
        pacmans = game_params["pacmans"]
        mp = game_params['map']

        self._in_progress = True
        self._pacmans = [Pacman(pacman[0], pacman[1]) for pacman in pacmans]
        self._maze = Maze(mp)

    @property
    def pacmans(self):
        return self._pacmans

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
        for pacman in self.pacmans:
            self.move(pacman)
            print(pacman.direction)
            print(pacman.position)
            print(id(pacman))
            if self.maze.has_coin(pacman.position):
                pacman.inc_score()
                self.maze.remove_coin(pacman.position)

    def to_params(self):
        spawns = self._maze.spawn_points
        width, height = self._maze.get_dimensions
        pacmans_count = self.pacmans.length
        return {
            "width": width,
            "height": height,
            "pacmans": [(i, point) for (i, point) in enumerate(spawns[1:pacmans_count+1], 1)]
        }

    def get(self):
        return self._maze

    def connect_pacman(self, pacman):
        self._pacmans.append(pacman)
