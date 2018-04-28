class Creature:
    def __init__(self, _id, pos):
        self._id = _id
        self.pos = pos
        self.direction = (0, 0)

    def move_up(self):
        self.direction = (-1, 0)

    def move_right(self):
        self.direction = (0, 1)

    def move_down(self):
        self.direction = (1, 0)

    def move_left(self):
        self.direction = (0, -1)

    def get_move(self):
        return [cur + nex for cur, nex in zip(self.pos, self.direction)]

    @property
    def position(self):
        return self.pos

    @property
    def id(self):
        return self._id

    def move(self):
        self.pos = [cur + nex for cur, nex in zip(self.pos, self.direction)]
        self.direction = (0, 0)
