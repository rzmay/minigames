# Robert May
# May 2018

from random import *
from minigame import *
from math import log
from timeit import default_timer as timer

class Coordgame(Minigame):
    def __init__(self, difficulty, rt):
        Minigame.__init__(self, difficulty, rt)
        self.chars = []
        chars = [chr(i) for i in range(ord('A'),ord('Z')+1)] + list("!@#$%&")
        # x and y axes
        self.axes = [chars[0:5],chars[0:5]]
        # characters used (index 0 = searched, index 1 = base)
        for i in range(0,2):
            char = choice(chars)
            self.chars.append(char)
            chars.remove(char)
        # number of shuffles
        self.shuffles = int(self.diff/2.2)
        self.shuffle()
        # answer to problem
        self.y = randint(0, 3)
        self.x = randint(0, 3)
        self.answer = self.axes[0][self.x] + self.axes[1][self.y]
        # create problem
        self.genProblem()

    def shuffle(self):
        while self.shuffles > 0:
            for axis in self.axes:
                i = 0
                while i < len(axis):
                    if randint(1, len(axis)) == 1:
                        self.shuffles -= 1
                        swapInd = randint(0, len(axis)-1)
                        while swapInd == i:
                            swapInd = randint(0, len(axis)-1)
                        temp = axis[i]
                        axis[i] = axis[swapInd]
                        axis[swapInd] = temp
                    i += 1


    def genProblem(self):
        arr = []
        for i  in range(0, 5):
            arr.append(self.chars[1] * 5 )
        tempRow = list(arr[self.y])
        tempRow[self.x] = self.chars[0]
        arr[self.y] = "".join(tempRow)
        self.lines = ["  %s"%("".join(self.axes[0])),
                      "",
                      self.axes[1][0] + " " + arr[0],
                      self.axes[1][1] + " " + arr[1],
                      self.axes[1][2] + " " + arr[2],
                      self.axes[1][3] + " " + arr[3],
                      self.axes[1][4] + " " + arr[4],
                      "",
                      "What are the",
                      "coordinates of",
                      "the character %s?"%(self.chars[0]),
                      "(in the form 'XY')"]


    def checkAnswer(self, answer, time):
        x = self.axes[0].index(answer[0])
        y = self.axes[1].index(answer[1])
        distance = ((x - self.x)**2 + (y - self.y)**2)**0.5
        difference = distance
        # "The answer was %s!"%(self.answer)
        self.difference = difference
        self.maxScore = self.getMaxScore()
        return self.getScore(time/2)

    def ask(self, style):
        self.displayLines(style)
        start = timer()
        answer = self.getCoord(range(ord("a"), ord("e") + 1))
        end = timer()
        score = self.checkAnswer(answer, (end - start))
        # "Your score:",score,"/",self.maxScore
        return score
