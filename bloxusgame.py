import copy
import random

import numpy as np


class Game():
    def show(self):
        if self.next_A:
            next = "A"
        else:
            next = "B"
        return "\n**********************\nMove {}\n".format(
            self.board.moves_count) + "Next to move: {}\n".format(
                next) + self.playerA.show() + self.playerB.show(
        ) + self.board.show()

    def __init__(self, playerA, playerB):
        self.board = Board()
        self.playerA = playerA
        self.playerB = playerB
        self.finished = False
        #self.next_A = bool(random.getrandbits(1))
        self.next_A = True
        self.game_state = [self.show()]
        self.game_end = 0

    def move(self, player, blox=None, x=None, y=None):

        if blox is None:
            move = player.getMove(self.board)
            if move:
                blox, x, y = move["blox"], move["x"], move["y"]
                self.game_end = 0
            else:
                self.game_end += 1
                if self.game_end > 3:
                    self.finished = True
                return
        correct_order = False
        if self.next_A and player is self.playerA:
            correct_order = True
        if not self.next_A and player is self.playerB:
            correct_order = True
        if correct_order:
            self.board.place_blox(blox, x, y)
            self.next_A = not self.next_A
            self.game_state.append(self.show())
        else:
            raise PermissionError("Wrong turn order!")

    def is_allowed(self, blox, x, y):
        self.board.is_allowed(blox, x, y)


class Player():
    def __init__(self, name, id, strategy=None):
        self.name = name
        self.id = id
        self.bloxs = []
        self.value = 0
        self.strategy = strategy
        self._add_blox("shapes.txt")

    def getMove(self, board):

        move = self.strategy(board, self.bloxs, self.id)
        if move:
            i = move["index"]
            blox = move["blox"]
            self.bloxs.pop(i)
            self.value -= blox.value
        return move

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
        s = ""
        for b in self.bloxs:
            s += b.show()
        return "Player {}\n".format(self.name) + "Hand value: {}\n".format(
            self.value) + s

    def rotate(self, i):
        self.bloxs[i].rotate()

    def flip(self, i):
        self.bloxs[i].flip()

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
        s = ""
        for row in self.body:
            s += "".join(str(int(i)) for i in row) + "\n"
        return "** {}:\n".format(self.value) + s + "\n"

    def rotate(self):
        self.body = np.rot90(self.body)

    def flip(self):
        self.body = np.fliplr(self.body)


class Board():
    def __init__(self):
        self.board = np.zeros((13, 13))
        self.moves_count = 0

    def show(self):
        s = ""
        for row in self.board:
            s += ("".join(str(int(i)) for i in row)) + "\n"
        return s

    def place_blox(self, blox, x, y):
        if not self._is_allowed(blox, x, y):
            raise RuntimeError("Illegal move")
        else:
            self._place(self.board, blox, x, y)
            self.moves_count += 1

    def _place(self, board, blox, x, y):
        for index, val in np.ndenumerate(blox.body):
            if val > 0:
                board[x + index[0]][y + index[1]] = val

    def _is_allowed(self, blox, x, y):
        lx, ly = np.shape(blox.body)
        if (x + lx > 13) or (y + ly > 13):
            return False
        if self._overlaps_element(blox, x, y):
            return False
        if self._is_illegal_initial_move(blox, x, y):
            return False
        if not self._is_adjacent_own_corner(blox, x, y):
            return False
        if self._is_adjacent_own_side(blox, x, y):
            return False
        return True

    def _covers_field(self, blox, x, y, px, py):
        if (px < x or py < y):
            return False
        if (px - x + 1 <= len(blox.body)) and (py - y + 1 <= len(
                blox.body[0])):
            return blox.body[px - x][py - y] > 0

    def _overlaps_element(self, blox, x, y):
        for index, val in np.ndenumerate(blox.body):
            if self._covers_field(
                    blox, x, y, x + index[0], y +
                    index[1]) and self.board[x + index[0]][y + index[1]] > 0:
                return True
        return False

    def _is_illegal_initial_move(self, blox, x, y):
        if self.moves_count < 2:
            if not (self._covers_field(blox, x, y, 4, 4)
                    or self._covers_field(blox, x, y, 9, 9)):
                return True
        return False

    def _is_adjacent_own_corner(self, blox, x, y):
        if self.moves_count < 2:
            return True
        vboard = np.zeros((16, 16))
        vboard[2:15, 2:15] = self.board
        x = x + 2
        y = y + 2
        self._place(vboard, blox, x, y)
        for index, val in np.ndenumerate(blox.body):
            if val > 0:
                if vboard[x + index[0] - 1][y + index[1] - 1] == val and \
                        vboard[x + index[0] - 1][y + index[1]] == 0 and \
                        vboard[x + index[0]][y + index[1] - 1] == 0:
                    return True
                if vboard[x + index[0] + 1][y + index[1] - 1] == val and \
                        vboard[x + index[0]][y + index[1] - 1] == 0 and \
                        vboard[x + index[0] + 1][y + index[1]] == 0:
                    return True
                if vboard[x + index[0] - 1][y + index[1] + 1] == val and \
                        vboard[x + index[0] - 1][y + index[1]] == 0 and \
                        vboard[x + index[0]][y + index[1] + 1] == 0:
                    return True
                if vboard[x + index[0] + 1][y + index[1] + 1] == val and \
                        vboard[x + index[0]][y + index[1] + 1] == 0 and \
                        vboard[x + index[0] + 1][y + index[1]] == 0:
                    return True
        return False

    def _is_adjacent_own_side(self, blox, x, y):
        if self.moves_count < 2:
            return False
        vboard = np.zeros((16, 16))
        vboard[2:15, 2:15] = self.board
        x = x + 2
        y = y + 2
        for index, val in np.ndenumerate(blox.body):
            if val > 0:
                if vboard[x + index[0] - 1][y + index[1]] == val or \
                        vboard[x + index[0]][y + index[1] - 1] == val or \
                        vboard[x + index[0]][y + index[1] + 1] == val or \
                        vboard[x + index[0]][y + index[1] + 1] == val:
                    return True
        return False
