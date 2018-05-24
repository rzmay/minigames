# Robert May
# May 2018

from random import *
from minigame import *
from math import log, ceil
from time import sleep
from timeit import default_timer as timer


class Fish:
    def __init__(self, rate, row):
        # Fish's position
        self.y = row
        self.x = float(randint(0, 7))
        # Fish's speed
        self.rate = rate
        self.tail = ">"
        self.points = int(row/2 + 10)
        if self.rate < 0:
            self.tail = "<"
    def update(self):
        self.x += self.rate
        if int(self.x) >= 8:
            self.x -= 8
        if int(self.x) < 0:
            self.x += 8
    def wasCaught(self):
        self.rate = 0
    def __str__(self):
        if self.rate > 0 or self.rate < 0:
            return "o"
        else:
            return "x"

class FishRod:
    def __init__(self, x, maxLen):
        self.x = x
        self.length = 0
        self.score = 0
        self.maxLen = maxLen
        self.fishCaught = 0
        self.chars = ["J"]
        self.isDropping = False
    def update(self, fishList):
        self.chars.insert(0, "|")
        self.length += 1
        self.caughtFish(fishList)
    def caughtFish(self, fishList):
        for fish in fishList:
            if (
                fish.rate != 0 and
                fish.y == self.length and int(fish.x) == self.x or
                fish.y == self.length and int(fish.x) + 1 == self.x or
                fish.y == self.length and int(fish.x) - 1 == self.x
               ):
                self.fishCaught += 1
                fish.wasCaught()
                self.score += fish.points


class Fishgame(Minigame):
    def __init__(self, difficulty, rt):
        Minigame.__init__(self, difficulty, rt)
        # number of rows
        self.rows = int(log(self.diff**4 + 2, 10))+2
        # later changed to sum of fish points
        self.answer = 0
        # Fishing rod
        self.rod = FishRod(randint(0, 7), self.rows)
        # Fish
        self.fishList = []
        # fishing area of self.lines
        self.lake = []
        # game instructions
        self.instructions = ["",
                             "Press [ENTER] to drop",
                             "drop the fishing line!"]
        # create problem
        self.genProblem()
        # speed of fish and rod
        self.gameTick = 1 / (self.diff / 2)
        if self.gameTick > 1:
            self.gameTick = 1

    def genProblem(self):
        self.lake = [[" "," "," "," "," "," "," "," "]]
        for i  in range(0, self.rows):
            self.lake.append(["~", "~", "~", "~", "~", "~", "~", "~"])
        self.lake[0][self.rod.x] = "v"
        row = 1
        while row <= self.rows:
            fishRate = randint(4, 8) / 8.0
            if randint(0, 1) == 0:
                fishRate *= -1
            self.fishList.append(Fish(fishRate,row))
            row += 1
        for fish in self.fishList:
            self.answer += fish.points

    def updateLake(self):
        self.lake = [[" "," "," "," "," "," "," "," "]]
        for i  in range(0, self.rows):
            self.lake.append(["~", "~", "~", "~", "~", "~", "~", "~"])
        self.lake[0][self.rod.x] = "v"
        for fish in self.fishList:
            fish.update()
        if self.rod.isDropping:
            self.rod.update(self.fishList)
        for fish in self.fishList:
            self.lake[fish.y][int(fish.x)] = str(fish)
            if fish.rate != 0:
                tailDir = int(fish.rate / abs(fish.rate)) * -1
                if (
                    int(fish.x) + tailDir < len(self.lake[fish.y]) and
                    int(fish.x) + tailDir >= 0
                    ):
                    self.lake[fish.y][int(fish.x) + tailDir] = fish.tail
        row = 0
        for char in self.rod.chars:
            if self.lake[row][self.rod.x] != "x":
                self.lake[row][self.rod.x] = char
            row += 1
        self.lines = []
        for row in self.lake:
            self.lines.append("".join(row))
        self.lines += self.instructions
        self.lines += ["Fish caught: " + str(self.rod.fishCaught)]

    def getMaxScore(self):
        return self.answer

    def checkAnswer(self, answer):
        self.maxScore = self.answer
        return answer

    def ask(self, style):

        enterPressed = False
        while self.rod.length < self.rod.maxLen:
            self.clearLines()
            self.updateLake()
            self.displayLines(style)

            if not enterPressed:
                enterPressed = self.enterCheck('', self.gameTick)
            else:
                sleep(self.gameTick)

            if enterPressed and not self.rod.isDropping:
                self.rod.isDropping = True


        self.rod.score *= int(ceil(self.diff/20))

        score = self.checkAnswer(self.rod.score)
        # print "Your score:",score,"/",self.maxScore
        return score
