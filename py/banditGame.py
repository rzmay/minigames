# Robert May
# May 2018

from random import random, choice, uniform, shuffle
from math import ceil
from minigame import *
import signal

class Toy:
    def __init__(self, chance):
        self.chance = chance
        self.disp = self.display(choice(["rattle",
                                        "doll",
                                        "balloon",
                                        "lollipop",
                                        "candy"]))
        self.width = max(len(self.disp[0]),
                         len(self.disp[1]),
                         len(self.disp[2]))
        self.height = len(self.disp)

    def display(self, dispType):
        dispDict = {"rattle":["  _",
                              " {~}",
                              " /"],
                    "candy":["",
                             ">[]<",
                             ""],
                    "balloon":["O",
                               "`",
                               " "],
                    "lollipop":["@",
                                "|",
                                ""],
                    "doll":[" O",
                            "-\\-",
                            " /\\"]}
        return dispDict[dispType]

    def play(self):
        return int(random() < self.chance)


class Baby:
    def __init__(self, toys):
        self.toys = []
        for i in range(0, toys-1):
            self.toys.append(Toy(uniform(0.0, 0.3)))
        self.toys.append(Toy(uniform(0.7, 1)))
        shuffle(self.toys)

        self.face = [" >&< ",
                     "(._.)",
                     "( _ )",
                     ""]
        self.trend = ""
        self.happiness = 5
        self.right = 0
        self.tries = 0

    def play(self, arm):
        ind = ord(arm.lower()) - 97
        result = self.toys[ind].play()
        self.trend = "+"
        if result == 0:
            self.happiness -= 1
            self.trend = "-"
        self.happiness += result
        self.right += result
        self.tries += 1
        self.face = [" >&< ",
                     "(._.)",
                     "( %s )"%(self.getSmile()),
                     ""]

    def getSmile(self):
        if self.happiness < 5:
            return "^"
        elif self.happiness < 10:
            return "_"
        else:
            return "v"
    def getFace(self):
        arr = []
        for i in range(0, 4):
            arr.append("   " + self.face[i])
        tempLine = list(arr[1])
        tempLine[1] = self.trend
        arr[1] = "".join(tempLine)
        return arr

    def getToyDisplay(self):
        arr = ["",
               "",
               "",
               "",
               ""]
        t = 0
        for toy in self.toys:
            l = 0
            for line in toy.disp:
                extra = toy.width - len(line) + 1
                arr[l] += line + " "*extra  + "  "
                l += 1
            arr[l] += " "*toy.width
            tempLine = list(arr[l])
            tempLine[-(int(ceil(toy.width/2.0)))] = chr(t + 65)
            arr[l] = "".join(tempLine)
            arr[l] += "   "
            t += 1
        return arr




class Banditgame(Minigame):
    def __init__(self, difficulty, rt):
        Minigame.__init__(self, difficulty, rt)
        toyNum = int((self.diff / 2) - 1)
        if toyNum < 2:
            toyNum = 2
        self.baby = Baby(toyNum)
        self.time = 5 + difficulty / 2
        self.maxScore = self.getMaxScore()
        self.instructions = ["Choose the toy that",
                             "the baby likes best",
                             "as many times as",
                             "you can!"]

    def getMaxScore(self):
        return self.baby.tries

    def checkAnswer(self):
        return self.baby.right

    def ask(self, style):
        signal.signal(signal.SIGALRM, self.alarmHandler)
        signal.setitimer(signal.ITIMER_REAL, self.time, self.time)
        try:
            while True:
                self.lines = self.baby.getFace() + self.baby.getToyDisplay() + self.instructions
                self.displayLines(style)
                self.baby.play(self.getLetter(range(97, 97 + len(self.baby.toys))))
        except AlarmException:
            pass
        signal.signal(signal.SIGALRM, signal.SIG_IGN)
        score = self.checkAnswer()
        # "Your score:",score,"/",self.maxScore
        return score
