# Robert May
# May 2018

from os import system
from timeit import default_timer as timer
from time import sleep
import signal
import sys
from random import choice


class AlarmException(Exception):
    pass


class Minigame:
    def __init__(self, difficulty, rt):
        # lines to be printed
        self.lines = []
        # difference from correct answer
        self.difference = 0
        # difficulty of game (suggested 1-10)
        self.diff = difficulty
        # maximum score
        self.maxScore = 0
        # number of lines printed in last display-lines
        self.lastLines = 0
        # require time for scoring?
        self.requireTime = rt
        # immutable display details
        self.style = ""
        self.styleLines = []
        self.width = 0
        self.availableSPace = 0
        self.startAt = 0
        self.suit = ""
        self.face = ""
    def getScore(self, time=None):
        if time is not None:
            timeDivisor = (float(time) / (self.diff / 3.9))
            if timeDivisor < 1:
                timeDivisor = 1
            score = ((self.diff * 50) / ((self.difference**2 + 0.2)**0.4)) / timeDivisor
        else:
            score = ((self.diff * 50) / ((self.difference**2 + 0.2)**0.4))
        return int(score)

    def alarmHandler(self, signum, frame):
        raise AlarmException

    def getDigit(self):
        dig = "a"
        while type(dig) is not int:
            try:
                dig = int(raw_input())
            except ValueError:
                print "Please enter a valid number."
        return int(dig)

    def getCoord(self, rang):
        coord = raw_input().lower()
        while (
                len(coord) != 2 or
                ord(coord[0]) not in range(ord('a'),ord('z')+1) or
                ord(coord[1]) not in range(ord('a'),ord('z')+1)or
                ord(coord[0]) not in rang or
                ord(coord[1]) not in rang
              ):
              coord = raw_input("Please enter a coordinate in the form 'xy'. ").lower()
        return coord.upper()

    def getLetter(self, rang):
        lett = raw_input().lower()
        while (
                len(lett) != 1 or
                ord(lett) not in rang
              ):
            lett = raw_input("Please enter a letter. ")
        return lett

    def getMaxScore(self):
        score = ((self.diff * 50) / ((0.2)**0.4))
        return int(score)

    def insertDetail(self):
        if self.style == "cards":
            for i in range(0, len(self.face)):
                tempLine = list(self.styleLines[i+1])
                tempLine[4] = self.face[i]
                self.styleLines[i+1] = "".join(tempLine)

                tempLine = list(self.styleLines[-(i + 4)])
                tempLine[-3] = self.face[i]
                self.styleLines[-(i+4)] = "".join(tempLine)
            tempLine = list(self.styleLines[1])
            tempLine[-3] = self.suit
            self.styleLines[1] = "".join(tempLine)

            tempLine = list(self.styleLines[-4])
            tempLine[4] = self.suit
            self.styleLines[-4] = "".join(tempLine)

    def displayLines(self, style):
        if style != self.style:
            self.style = style
            if style == "crystal-ball":
                self.styleLines = ["        . -- ~~~ -- .",
                              "    .-~               ~-.",
                              "   /                     \\",
                              "  /                       \\",
                              " |                         |",
                              " |                         |",
                              " |                         |",
                              "  \\                       /",
                              "   \\                     /",
                              "    `-.               .-'",
                              "        ~- . ___ . -~",
                              "       /              \\",
                              "      /~-.___________.-~\\"]
                self.availableSpace = 9
                self.width = len(self.styleLines[4])
                self.startAt = 1
                self.copyLine = " |                         |"
            elif style == "palm":
                self.styleLines = ["          /\"\\",
                              "      /\"\\|   |/\"\\",
                              "     |   |   |   |",
                              "     |   |   |   |",
                              "     |   |>~<|   |/\"\\",
                              "     |>~<|   |>~<|   |",
                              "     |   |   |   |   |",
                              " /~T\\|   |   |   |   |",
                              " |   |   |   |   |   |",
                              " |   | ~   ~   ~ |   |",
                              " |~< |             ~ |",
                              "|                     |",
                              "|                     |",
                              "|                     |",
                              "\\                     |",
                              " \\                   /",
                              "  \\                 /",
                              "   \\.              /",
                              "     |            |",
                              "     |            |"]
                self.availableSpace = 6
                self.width = len(self.styleLines[11])
                self.startAt = 11
                self.copyLine = "|                     |"
            elif style == "constellations":
                self.styleLines = ["                 '",
                              "            *          .",
                              "                   *       ' ",
                              "              *                *",
                              "                                ",
                              "   *                            ",
                              "                                ",
                              "                                ",
                              "      '                         ",
                              "                                ",
                              "                           *    ",
                              "                                ",
                              "                                ",
                              "   *   '*",
                              "           *",
                              "                *        ",
                              "                       *",
                              "               *  ",
                              "                     *"]
                self.availableSpace = 9
                self.width = len(self.styleLines[4])
                self.startAt = 4
                self.copyLine = "                                "
            elif style == "cards":
                self.styleLines = ["  +------------------------------+",
                              "  |                              |",
                              "  |    ----------------------    |",
                              "  |   |                      |   |",
                              "  |   |                      |   |",
                              "  |   |                      |   |",
                              "  |   |                      |   |",
                              "  |   |                      |   |",
                              "  |   |                      |   |",
                              "  |   |                      |   |",
                              "  |   |                      |   |",
                              "  |   |                      |   |",
                              "  |   |                      |   |",
                              "  |   |                      |   |",
                              "  |    ----------------------    |",
                              "  |                              |",
                              "  +------------------------------+",
                              "  |------------------------------|",
                              "  +------------------------------+"]
                self.availableSpace = 11
                self.width = len(self.styleLines[4])
                self.startAt = 3
                self.copyLine = "  |   |                      |   |"
                self.face = choice(["THE STAR","THE WORLD","THE FOOL",
                                    "THE HIEROPHANT","THE CHARIOT","THE HERMIT",
                                    "THE MAGICIAN", "JOKER"])
                self.suit = {"THE STAR":"*","THE WORLD":"@","THE FOOL":"?",
                             "THE HIEROPHANT":"$","THE CHARIOT":"!","THE HERMIT":"%",
                             "THE MAGICIAN":"+","JOKER":"E"}[self.face]

        if len(self.lines) > self.availableSpace:
            for i in range(0, len(self.lines) - self.availableSpace):
                self.styleLines.insert(self.availableSpace/2 + self.startAt, self.copyLine)
                self.availableSpace += 1
        cuRow = (self.availableSpace - len(self.lines))/2 + self.startAt
        for line in self.lines:
            tempLine = list(self.styleLines[cuRow])
            tempLine[(self.width - len(line))/2 + 1:(self.width - len(line))/2+len(line) + 1] = line
            self.styleLines[cuRow] = "".join(tempLine)
            cuRow += 1
        self.insertDetail()
        for line in self.styleLines:
            print line
        self.lastLines = len(self.styleLines)

    def enterCheck(self, prompt, timeout):
        signal.signal(signal.SIGALRM, self.alarmHandler)
        signal.setitimer(signal.ITIMER_REAL, timeout, timeout)
        start = timer()
        try:
            raw_input()
            self.lastLines += 1
            signal.setitimer(signal.ITIMER_REAL, 0)
            end = timer()
            remainingTime = timeout - (end-start)
            if remainingTime > 0:
                self.enterCheck('', remainingTime)
            return True
        except AlarmException:
            pass
        signal.signal(signal.SIGALRM, signal.SIG_IGN)
        return False
    def clearLines(self):
        for i in range(self.lastLines):
            sys.stdout.write("\033[F")
