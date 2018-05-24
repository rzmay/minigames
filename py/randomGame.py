# Robert May
# May 2018

from random import choice
from mathGame import *
from memoryGame import *
from countGame import *
from coordGame import *
from fishGame import *
from hurdleGame import *
from flyingGame import *
from banditGame import *

class Game:
    def __init__(self, difficulty, rt):
        self.game = choice([Mathgame(difficulty, rt),
                            Memorygame(difficulty, rt),
                            Countgame(difficulty, rt),
                            Coordgame(difficulty, rt),
                            Fishgame(difficulty, rt),
                            Hurdlegame(difficulty, rt),
                            Flyinggame(difficulty, rt),
                            Banditgame(difficulty, rt)])

    def getMaxScore(self):
        return self.game.getMaxScore()

    def ask(self, style):
        return self.game.ask(style)
