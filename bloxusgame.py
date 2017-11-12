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
        self.bloxs = []
        self.value = 0
        self._add_blox(Blox([[0, 0], [0, id]], 1))
        self._add_blox(Blox([[id, id, id, id]], 4))
        self._add_blox(Blox([[0, id, 0, 0], [id, id, id, id]], 5))

    def _add_blox(self, blox):
        self.value += blox.value
        self.bloxs.append(blox)

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
        try:
            self.is_allowed(blox, x, y)
        except RuntimeError:
            print("Illegal move")
        else:
            for index, val in np.ndenumerate(blox.body):
                self.board[x + index[0]][y + index[1]] = val
            if self.first_move > 0:
                self.first_move -= 1

    def is_allowed(self, blox, x, y):

        return True
