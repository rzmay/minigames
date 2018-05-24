# Robert May
# May 2018

from random import *
from minigame import *
from math import log
from timeit import default_timer as timer

class Countgame(Minigame):
    def __init__(self, difficulty, rt):
        Minigame.__init__(self, difficulty, rt)
        # characters used (index 0 = counted, index 1 = base)
        self.chars = []
        chars = [chr(i) for i in range(ord('A'),ord('Z')+1)] + list("!@#$%&")
        for i in range(0,2):
            char = choice(chars)
            self.chars.append(char)
            chars.remove(char)
        # number of rows
        self.rows = int(log(self.diff**4 + 2, 10))+1
        # answer to problem
        self.answer = 0
        # create problem
        self.genProblem()

    def genProblem(self):
        arr = []
        for i  in range(0, self.rows):
            arr.append([0, 0, 0, 0, 0, 0, 0, 0])
        row = 0
        while row < len(arr):
            for i in range(0,8):
                arr[row]
                if randint(0,2) == 0:
                    arr[row][i] = self.chars[0]
                    self.answer += 1
                else:
                    arr[row][i] = self.chars[1]
            self.lines.append("".join(arr[row]))
            row += 1
        nextLines = ["",
                     "How many %s's"%(self.chars[0]),
                     "appeared in the",
                     "above sequence?"]
        self.lines += nextLines

    def checkAnswer(self, answer, time):
        difference = self.answer - answer
        # print "The answer was %s!"%(self.answer)
        if difference < 0:
            difference *= -1
        self.difference = difference
        self.maxScore = self.getMaxScore()
        return self.getScore(time/5)

    def ask(self, style):
        self.displayLines(style)
        start = timer()
        answer = self.getDigit()
        end = timer()
        score = self.checkAnswer(answer, (end - start))
        # print "Your score:",score,"/",self.maxScore
        return score
