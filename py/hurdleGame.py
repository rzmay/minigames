# Robert May
# May 2018

from random import *
from minigame import *
from math import log, ceil
from time import sleep
from timeit import default_timer as timer


class Hurdle:
    def __init__(self, row, distance):
        # hurdle's position
        self.height = row
        self.x = distance
        # was the hurdle hit?
        self.wasHit = False

    def wasCaught(self, x, y):
        if not self.wasHit:
            if x == self.x and y >= self.height:
                self.wasHit = True
                return True


class Runner:
    def __init__(self, groundIndex):
        self.x = 0
        self.y = groundIndex
        self.g = 13.0
        self.ground = groundIndex
        self.yVelocity = 0
        self.score = 0
        self.groundChars = [[" o ",
                             "_|-"],
                            [" o ",
                             "-|-"],
                            [" o ",
                             "-|_"],
                            [" o ",
                             "_|_"]]
        self.jumpChars = [[" o ",
                           "/|\\"],
                          [" o ",
                           "\\|/"]]
        self.currentSprite = []
        self.animFrame = 0
        self.inAir = False

    def update(self, hurdleList):
        tick = 0.2
        if self.inAir:
            self.currentSprite = self.jumpChars[0]
            self.updateY(tick)
        else:
            self.animFrame += 1
            if self.animFrame >= len(self.groundChars):
                self.animFrame = 0
            self.currentSprite = self.groundChars[self.animFrame]
        self.x += 1
        self.hitHurdle(hurdleList)

    def getScore(self, hurdleList):
        for hurdle in hurdleList:
            self.score += hurdle.height

    def updateY(self, tick):
        self.y += self.yVelocity * tick
        self.yVelocity += self.g * tick
        if self.y > self.ground:
            self.y = self.ground
            self.inAir = False
        if int(self.yVelocity) > 0:
            self.currentSprite = self.jumpChars[1]


    def jump(self):
        if not self.inAir:
            self.yVelocity = -10
            self.inAir = True

    def hitHurdle(self, hurdleList):
        for hurdle in hurdleList:
            cuX = self.x
            cuY = int(self.y)
            for j in range(cuY - 1, cuY + 1):
                for k in range(cuX, cuX + 3):
                    if (
                        j > self.ground - hurdle.height and
                        k == hurdle.x and
                        not hurdle.wasHit
                        ):
                        hurdle.wasHit = True
                        self.score -= hurdle.height



class Track:
    def __init__(self, length, maxHeight):
        # length of track
        self.length = length
        # hurdles
        self.hurdleList = []
        # width of challenging track (stops 20 after last hurdle)
        self.width = 0
        if length/10 < 5:
            hurdleNum = 5
        else:
            hurdleNum = randint(5, length/10)
        self.length += 3 * hurdleNum
        self.gameFinished = False

        if maxHeight <= 2:
            self.maxHeight = 2
        elif maxHeight >=4:
            self.maxHeight = 4
        else:
            self.maxHeight = int(maxHeight)

        self.track = self.generateTrack(hurdleNum)
        self.visible = self.track[0:20]
        self.runner = Runner(len(self.track) - 2)
        self.runner.getScore(self.hurdleList)

    def generateTrack(self, hurdleNum):
        avgBetween = (self.length - 10) / hurdleNum
        coord = 10
        if self.hurdleList == []:
            for i in range(hurdleNum):
                coord += 3
                height = randint(2, self.maxHeight)
                dist = coord + randint(5 * ceil(height/3.0), avgBetween)
                self.hurdleList.append(Hurdle(height, dist))
                coord = dist
                self.width = dist+5
        arr = []
        for i in range(0, 10):
            arr.append(" "*(self.width + 25))
        arr.append("~"*(self.width + 25))
        return arr

    def insertHurdle(self, hurdle):
        if hurdle.wasHit:
            coord = hurdle.x + 2
            tempLine = list(self.track[-2])
            for i in range(0, hurdle.height - 1):
                tempLine[coord] = "-"
                coord += 1
            self.track[-2] = "".join(tempLine)
            tempLine = list(self.track[-2])
            tempLine[coord + 1] = "|"
            self.track[-2] = "".join(tempLine)
        else:
            coord = hurdle.height
            tempLine = list(self.track[-(coord + 1)])
            tempLine[hurdle.x] = "_"
            self.track[-(coord + 1)] = "".join(tempLine)
            for i in range(0,hurdle.height):
                tempLine = list(self.track[-(coord)])
                tempLine[hurdle.x] = "|"
                self.track[-(coord)] = "".join(tempLine)
                coord -= 1

    def insertRunner(self):
        # set legs
        tempLine = list(self.track[int(self.runner.y)])
        tempLine[self.runner.x:self.runner.x+3] = self.runner.currentSprite[1]
        self.track[int(self.runner.y)] = "".join(tempLine)
        # set head
        tempLine = list(self.track[int(self.runner.y) - 1])
        tempLine[self.runner.x:self.runner.x+3] = self.runner.currentSprite[0]
        self.track[int(self.runner.y) - 1] = "".join(tempLine)

    def updateTrack(self):
        # reset track
        self.track = self.generateTrack(len(self.hurdleList))
        # update runner, check collisions
        self.runner.update(self.hurdleList)
        # insert hurdles
        for hurdle in self.hurdleList:
            self.insertHurdle(hurdle)
        # insert runner
        self.insertRunner()
        if self.runner.x + 20 <= len(self.track[0]):
            # set visible part of track
            self.visible = []
            for i in self.track:
                self.visible.append(i[self.runner.x:self.runner.x+20])
        else:
            #end game
            self.gameFinished = True





class Hurdlegame(Minigame):
    def __init__(self, difficulty, rt):
        Minigame.__init__(self, difficulty, rt)
        # number of rows
        self.length = (int(log(self.diff**4 + 2, 10))+2) * 14
        self.track = Track(self.length, difficulty / 1.5)
        self.answer = self.track.runner.score
        # game instructions
        self.instructions = ["",
                             "Press [ENTER] to jump",
                             "over the hurdles!"]
        self.gameTick = 1 / (self.diff * 2)
        if self.gameTick > 0.3:
            self.gameTick = 0.3

    def getMaxScore(self):
        return self.answer

    def checkAnswer(self, answer):
        self.maxScore = self.answer
        return answer

    def updateLines(self):
        self.track.updateTrack()
        self.lines = self.track.visible + self.instructions

    def ask(self, style):

        enterPressed = False
        while not self.track.gameFinished:
            self.clearLines()
            self.updateLines()
            self.displayLines(style)

            if not enterPressed:
                enterPressed = self.enterCheck('', self.gameTick)
            else:
                enterPressed = False
                sleep(self.gameTick)
                self.track.runner.jump()


        self.track.runner.score *= int(ceil(self.diff/20))

        score = self.checkAnswer(self.track.runner.score)
        # print "Your score:",score,"/",self.maxScore
        return score
