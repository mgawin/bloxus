import numpy as np
import io


class Game():
    def __init__(self):
        self.board = Board()
        self.playerA = Player("A", 1)
        self.playerB = Player("B", 2)

    def show(self):
        self.playerA.show()
        self.playerB.show()
        self.board.show()

    def move(self, blox, x, y):
        self.board.place(blox, x, y)

    def is_allowed(self, blox, x, y):
        self.board.is_allowed(blox, x, y)


class Player():
    def __init__(self, name, id):
        self.name = name
        self.bloxs = []
        self.value = 0
        self._add_blox("shapes.txt")

    def _add_blox(self, filename):
        with open(filename, "r") as fp:
            element = []
            val = 0
            lines = fp.readlines()
            for line in lines:
                if line.count("0") + line.count("1") + line.count("\n") != len(
                        line):
                    raise RuntimeError("Invalid block shapes file.")
                if line[0] == "\n" or line.index == len(lines) - 1:
                    self.bloxs.append(Blox(element, val))
                    self.value += val
                    element = []
                    val = 0
                    continue
                val += line.count("1")
                row = [int(i) for i in list(line.strip())]
                element.append(row)
            if len(element) > 0:
                self.bloxs.append(Blox(element, val))
                self.value += val

    def show(self):
        print("Player {}".format(self.name))
        print("Hand value: {}".format(self.value))
        for b in self.bloxs:
            b.show()

    def rotate(self, i):
        self.bloxs[i].rotate()

    def put(self, i):
        blox = self.bloxs[i]
        self.bloxs.pop(i)
        self.value -= blox.value
        return blox


class Blox():
    def __init__(self, shape, value):
        self.body = np.array(shape)
        self.value = value

    def show(self):
        print("** {}:".format(self.value))
        print(self.body, "\n")

    def rotate(self):
        self.body = np.rot90(self.body)

    def flip(self):
        self.body = np.fliplr(self.body)


class Board():
    def __init__(self):
        self.board = np.zeros((13, 13))
        self.first_move = 2

    def show(self):
        print(self.board)

    def place(self, blox, x, y):
        if not self._is_allowed(blox, x, y):
            raise RuntimeError("Illegal move")
        else:
            for index, val in np.ndenumerate(blox.body):
                self.board[x + index[0]][y + index[1]] = val
            if self.first_move > 0:
                self.first_move -= 1

    def _is_allowed(self, blox, y, x):
        ly, lx = np.shape(blox.body)
        if (x + lx > 13) or (y + ly > 13):
            return False
        return True
