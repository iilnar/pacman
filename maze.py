import copy


class Maze:
    def __init__(self, mp):
        self._board = mp

    @property
    def board(self):
        return copy.deepcopy(self._board)

    def is_wall(self, pos):
        return self._board[pos[0]][pos[1]] == '#'

    def remove_coin(self, pos):
        if self._board[pos[0]][pos[1]] == '.':
            self._board[pos[0]][pos[1]] = ' '

    def has_coin(self, pos):
        return self._board[pos[0]][pos[1]] == '.'

    def __str__(self):
        board = copy.deepcopy(self._board)
        return "\n".join(" ".join(s) for s in board)
