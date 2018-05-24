# Robert May
# May 2018

from random import *
from minigame import *
from math import log, ceil
from time import sleep
from timeit import default_timer as timer

class Bird:
    def __init__(self, row, distance):
        # bird position
        self.y = row
        self.x = distance + 5
        # was the bird hit?
        self.wasHit = False
        self.chars =["^v^",
                     "-v-"]
        self.deadChars = "\\v/"
        self.currentSprite = ""
        self.animFrame = 0

    def update(self):
        if self.wasHit and self.y < 10:
            self.currentSprite = self.deadChars
            self.y += 1
        elif self.y == 10:
            self.currentSprite = "_._"
        else:
            self.currentSprite = self.chars[self.animFrame]
            self.animFrame += 1
            if self.animFrame > 1:
                self.animFrame = 0


class Balloon:
    def __init__(self, groundIndex):
        self.x = 2
        self.y = groundIndex / 2
        self.g = 4.3
        self.ground = groundIndex
        self.yVelocity = 0
        self.score = 0
        self.chars = ["O",
                      "'"]
        self.popChars = ["*",
                         ","]
        self.frame = 1
    def update(self, birdList):
        tick = 0.2

        self.updateY(tick)

        self.x += 1
        self.hitBird(birdList)

    def getScore(self, birdList):
        self.score = len(birdList)

    def updateY(self, tick):
        self.y += self.yVelocity * tick
        if self.y > self.ground:
            self.y = self.ground
        else:
            self.yVelocity += self.g * tick
        if self.yVelocity > 5:
            self.yVelocity = 5
        if self.y - 1 < 1:
            self.y = 1

    def conclude(self):
        self.chars = self.popChars


    def rise(self):
        if self.y - 1 >= 1 and self.yVelocity < 10:
            self.yVelocity -= self.g

    def hitBird(self, birdList):
        for bird in birdList:
            for i in range(bird.x, bird.x + 3):
                if i == self.x and bird.y == int(self.y) - 1 and not bird.wasHit:
                    self.score -= 1
                    bird.wasHit = True



class Sky:
    def __init__(self, length):
        # length of track
        self.length = length
        # birds
        self.birdList = []
        # width of challenging track (stops 20 after last bird)
        self.width = 0
        if length/3 < 10:
            birdNum = 10
        else:
            birdNum = randint(10, length/3)
        self.balloon = Balloon(10)
        self.gameFinished = False
        self.track = self.generateSky(birdNum)
        self.visible = self.track[0:20]
        self.balloon.getScore(self.birdList)

    def generateSky(self, birdNum):
        placementRate = birdNum / (10.0 * self.length)
        coord = 5
        arr = []
        for i in range(0, 10):
            arr.append(" "*(self.length + 30))
        if self.birdList == []:
            while len(self.birdList) < birdNum:
                row = 0
                for r in arr:
                    col = 0
                    for c in r:
                        num = randint(0, int(1 / placementRate))
                        if col > 19 and col < self.length and num == 0:
                            self.birdList.append(Bird(row, col))
                        col += 1
                    row += 1
        arr.append("~"*(self.length + 30))
        return arr

    def insertBird(self, bird):
        tempRow = list(self.track[bird.y])
        tempRow[bird.x:bird.x+3] = bird.currentSprite
        self.track[bird.y] = "".join(tempRow)

    def insertBalloon(self):
        # set string
        tempLine = list(self.track[int(self.balloon.y)])
        tempLine[self.balloon.x] = self.balloon.chars[1]
        self.track[int(self.balloon.y)] = "".join(tempLine)
        # set balloon
        tempLine = list(self.track[int(self.balloon.y-1)])
        tempLine[self.balloon.x] = self.balloon.chars[0]
        self.track[int(self.balloon.y-1)] = "".join(tempLine)

    def updateTrack(self):
        # reset track
        self.track = self.generateSky(len(self.birdList))
        # update runner, check collisions
        if self.balloon.x + 20 <= len(self.track[0]):
            self.balloon.update(self.birdList)
            # insert birds
            for bird in self.birdList:
                # update bird
                bird.update()
                self.insertBird(bird)
            # insert balloon
            self.insertBalloon()
        else:
            #end game
            self.balloon.x = len(self.track[0]) - 19
            self.conclude(self.balloon.frame)
            self.balloon.y += 1
            self.balloon.frame += 1
            if self.balloon.frame == 3:
                sleep(0.5)
        # set visible part of track
        self.visible = []
        for i in self.track:
            self.visible.append(i[self.balloon.x - 5:self.balloon.x+15])


    def conclude(self, frame):
        if frame == 1:
            self.track = self.generateSky(len(self.birdList))
            self.balloon.conclude()
            self.insertBalloon()

        elif self.balloon.y + 1 < len(self.track):
            self.track = self.generateSky(len(self.birdList))
            self.balloon.chars = [" ","~"]
            self.insertBalloon()

        else:
            self.gameFinished = True






class Flyinggame(Minigame):
    def __init__(self, difficulty, rt):
        Minigame.__init__(self, difficulty, rt)
        # number of rows
        self.length = (int(log(self.diff**4 + 2, 10))+2) * 17
        # later changed to sum of fish points
        self.sky = Sky(self.length)
        self.answer = self.sky.balloon.score
        # game instructions
        self.instructions = ["",
                             "Press [ENTER] to rise!",
                             "avoid the birds!"]
        self.gameTick = 1 / (self.diff * 20) ** 0.5
        if self.gameTick > 0.3:
            self.gameTick = 0.3

    def getMaxScore(self):
        return self.answer

    def checkAnswer(self, answer):
        self.maxScore = self.answer
        return answer

    def updateLines(self):
        self.sky.updateTrack()
        self.lines = self.sky.visible + ["|Velocity: %s |"%(round(-1*self.sky.balloon.yVelocity, 3))] + self.instructions


    def ask(self, style):

        enterPressed = False
        while not self.sky.gameFinished:
            self.clearLines()
            self.updateLines()
            self.displayLines(style)
            # for line in self.sky.track:
            #     print "".join(line)

            if not enterPressed:
                enterPressed = self.enterCheck('', self.gameTick)
            else:
                enterPressed = False
                sleep(self.gameTick)
                self.sky.balloon.rise()


        self.sky.balloon.score *= int(ceil(self.diff/20))

        score = self.checkAnswer(self.sky.balloon.score)
        # print "Your score:",score,"/",self.maxScore
        return score
