# Robert May
# May 2018

from random import *
from minigame import *
from time import *
from timeit import default_timer as timer
import os

class Memorygame(Minigame):
    def __init__(self, difficulty, rt):
        Minigame.__init__(self, difficulty, rt)
        # type of equation
        self.cards = []
        chars = [chr(i) for i in range(ord('A'),ord('Z')+1)] + list("!@#$%&")
        for i in range(0,4):
            char = choice(chars)
            self.cards.append(char)
            chars.remove(char)
        # answer to problem
        self.answer = randint(1, 4)
        self.time = int(25 / (self.diff + 4))
        if self.time < 3:
            self.time = 3

    def checkAnswer(self, answer, time):
        difference = self.answer - answer
        # print "The answer was %s!"%(self.answer)
        if difference < 0:
            difference *= -1
        self.difference = difference * 3
        self.maxScore = self.getMaxScore()
        return self.getScore()

    def wait(self, time):
        os.system("read -t %s discard"%(time))

    def ask(self, style):
        self.lines = ["|%s| |%s| |%s| |%s|"%(self.cards[0], self.cards[1], self.cards[2], self.cards[3]),
                      "",
                      "Observe the deck",
                      "of cards above.",
                      "Wait..."]
        self.displayLines(style)
        self.wait(self.time)
        self.clearLines()
        self.lines = ["|1| |2| |3| |4|",
                      "",
                      "Which card held",
                      "the character %s?"%(self.cards[self.answer-1]),
                      "Select 1, 2, 3 or 4"]
        self.displayLines(style)
        start = timer()
        answer = self.getDigit()
        end = timer()
        score = self.checkAnswer(answer, end - start)
        # print "Your score:",score,"/",self.maxScore
        return score
