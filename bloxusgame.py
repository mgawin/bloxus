import numpy as np


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
        self.id = id
        self.bloxs = []
        self.value = 0
        self._add_blox("shapes.txt")

    def _add_blox(self, filename):
        with open(filename, "r") as fp:
            element = []
            val = 0
            for line in fp:
                if line.count("0") + line.count("1") + line.count("\n") != len(
                        line):
                    raise RuntimeError("Invalid block shapes file.")
                if line[0] == "\n":
                    self.bloxs.append(Blox(element, val))
                    self.value += val
                    element = []
                    val = 0
                    continue
                val += line.count("1")
                row = [
                    int(i)
                    for i in list(line.strip().replace('1', str(self.id)))
                ]
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
        self.moves_count = 0

    def show(self):
        print(self.board)

    def place(self, blox, x, y):
        if not self._is_allowed(blox, x, y):
            raise RuntimeError("Illegal move")
        else:
            for index, val in np.ndenumerate(blox.body):
                self.board[x + index[0]][y + index[1]] = val
            self.moves_count += 1

    def _is_allowed(self, blox, x, y):
        ly, lx = np.shape(blox.body)
        if (x + lx > 13) or (y + ly > 13):
            return False
        if self._overlaps_element(blox, x, y):
            return False
        if self._is_illegal_initial_move(blox, x, y):
            return False
        return True

    def _covers_field(self, blox, x, y, px, py):
        if (px < x or py < y):
            return False
        if (px - x <= len(blox.body)) and (py - y <= len(blox.body[0])):
            return blox.body[px - x][py - y] > 0

    def _overlaps_element(self, blox, x, y):
        for index, val in np.ndenumerate(blox.body):
            if self._covers_field(
                    blox, x, y, x + index[0], y +
                    index[1]) and self.board[x + index[0]][y + index[1]] > 0:
                return True
        return False

    def _is_illegal_initial_move(self, blox, x, y):
        print(self.moves_count)
        blox.show()
        print(x, y)
        if self.moves_count < 2:
            if not (self._covers_field(blox, x, y, 9, 6)
                    or self._covers_field(blox, x, y, 6, 9)):
                return True
        return False
