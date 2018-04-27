import copy


class Maze:
    def __init__(self, n, m, pacman):
        self.board = [['#'] + ['.'] * m + ['#'] for _ in range(m)]
        self.board = [['#'] * (m + 2)] + self.board + [['#'] * (m + 2)]
        self.pacman = pacman

    def set_pacman(self, pos):
        self.pacman = pos

    def is_wall(self, pos):
        return self.board[pos[0]][pos[1]] == '#'

    def __str__(self):
        board = copy.deepcopy(self.board)
        board[self.pacman[0]][self.pacman[1]] = 'P'
        return "\n".join(" ".join(s) for s in board)
