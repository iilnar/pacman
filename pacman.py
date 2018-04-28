from creature import Creature

class Pacman(Creature):
    def __init__(self, idd, pos):
        super(Pacman, self).__init__(idd, pos)
        self.superpower = 0
        self.score = 0

    def inc_score(self):
        self.score += 1

    def set_superpower(self, duration):
        self.superpower += duration

    def dec_superpower(self):
        self.superpower = max(0, self.superpower - 1)
