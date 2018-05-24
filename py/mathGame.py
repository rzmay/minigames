# Robert May
# May 2018

from random import *
from minigame import *
from timeit import default_timer as timer

class Mathgame(Minigame):
    def __init__(self, difficulty, rt):
        Minigame.__init__(self, difficulty, rt)
        # type of equation
        self.type = choice(["Add", "Sub", "Mult", "Div"])
        # answer to problem
        self.answer = 0
        # create problem
        self.genProblem()
    def genAdd(self):
        addend1 = randint(0, int(self.diff * 20))
        addend2 = randint(0, int(self.diff * 10))
        answer = addend1 + addend2
        self.lines = ["%s + %s = ?" %(addend1, addend2),
                      "",
                      "What is the answer?"]
        self.answer = answer
    def genSub(self):
        addend1 = randint(0, int(self.diff * 20))
        addend2 = randint(0, int(self.diff * 10))
        answer = addend1 - addend2
        self.lines = ["%s - %s = ?" %(addend1, addend2),
                      "",
                      "What is the answer?"]
        self.answer = answer
    def genMult(self):
        factor1 = randint(0, int(self.diff * 10))
        factor2 = randint(0, int(self.diff * 5))
        product = factor1 * factor2
        self.lines = ["%s x %s = ?" %(factor1, factor2),
                      "",
                      "What is the answer?"]
        self.answer = product
    def genDiv(self):
        factor1 = randint(1, int(self.diff * 10))
        factor2 = randint(1, int(self.diff * 5))
        product = factor1 * factor2
        self.lines = ["%s / %s = ?" %(product, factor2),
                      "",
                      "What is the answer?"]
        self.answer = factor1
    def genProblem(self):
        getattr(self, "gen" + self.type)()
    def checkAnswer(self, answer, time):
        difference = self.answer - answer
        # print "The answer was %s!"%(self.answer)
        if difference < 0:
            difference *= -1
        self.difference = difference
        self.maxScore = self.getMaxScore()
        return self.getScore(time/3)
    def ask(self, style):
        self.displayLines(style)
        start = timer()
        answer = self.getDigit()
        end = timer()
        score = self.checkAnswer(answer, end - start)
        # print "Your score:",score,"/",self.maxScore
        return score
