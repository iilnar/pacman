from random import randint
class Creature:
    def __init__(self, _id, pos):
        self._id = _id
        self.pos = pos
        self.direction = (0, 0)
        color = randint(0, 0xffffff)
        self.color = '#%06x' % color

    def move_up(self, world=None):
        if self.direction != (0, 0):
            return
        self.direction = (-1, 0)

    def move_right(self, world=None):
        if self.direction != (0, 0):
            return
        self.direction = (0, 1)

    def move_down(self, world=None):
        if self.direction != (0, 0):
            return
        self.direction = (1, 0)

    def move_left(self, world=None):
        if self.direction != (0, 0):
            return
        self.direction = (0, -1)

    def get_move(self, world=None):
        return [cur + nex for cur, nex in zip(self.pos, self.direction)]

    @property
    def position(self):
        return self.pos

    @property
    def id(self):
        return self._id

    def move(self, world=None):
        self.pos = [cur + nex for cur, nex in zip(self.pos, self.direction)]
        self.direction = (0, 0)
