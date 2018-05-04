from creature import Creature

class Pacman(Creature):
    def __init__(self, idd, pos):
        super(Pacman, self).__init__(idd, pos)
        self.score = 0

    def inc_score(self):
        self.score += 1
