import uuid
import numpy as np
from bloxus_lib import bloxusdb as db
import os.path


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
        self.next_A = True
        self.id = str(uuid.uuid4()).replace("-", "")
        self.game_end = 0
        self.move_history = []
        self.move_history_len = 40

    def get_player(self, id):
        if self.playerA.id == id:
            return self.playerA
        elif self.playerB.id == id:
            return self.playerB
        else:
            raise RuntimeError("Non-existing player id value.")

    def move(self, player, move=None):
        if move is None:
            move = player.getMove(self.board)
        if move:
            id, x, y, rotates, flip = move["id"], move["x"], move[
                "y"], move["rotates"], move["flip"]
            blox = player.put(id)
            if rotates > 0:
                blox.rotate(rotates)
            if flip:
                blox.flip()
            self.game_end = 0
        else:
            self.game_end += 1
            if self.game_end > 3:
                self.finished = True
                self.playerA.calculate_score()
                self.playerB.calculate_score()
                db.store_game(self)
            return
        correct_order = False
        if self.next_A and player is self.playerA:
            correct_order = True
        if not self.next_A and player is self.playerB:
            correct_order = True
        if correct_order:
            self.board.place_blox(blox, x, y)
            self.next_A = not self.next_A
            move['player'] = player.id
            db.store_move(self.id, move)
            self._add_to_history(
                {"player_id": player.id, "blox": blox, "x": x, "y": y})
        else:
            raise PermissionError("Wrong turn order!")

    def undo_move(self):
        if len(self.move_history) > 0:
            move = self.move_history[0]
            player = self.get_player(move["player_id"])
            blox = move["blox"]
            x = move["x"]
            y = move["y"]
            self.board.remove_blox(blox, x, y)
            del self.move_history[0]
            player.get_back(blox)
            self.next_A = not self.next_A
            return True

        return False

    def is_allowed(self, blox, x, y):
        self.board.is_allowed(blox, x, y)

    def _add_to_history(self, move):
        self.move_history.insert(0, move)
        if len(self.move_history) > self.move_history_len:
            del self.move_history[-1]


class Player():
    def __init__(self, name, id, strategy=None):
        self.name = name
        self.id = id
        self.bloxs = []
        self.value = 0
        self.strategy = strategy
        shape_path = os.path.join(
            os.path.dirname(__file__), "./res/shapes.txt")
        self._add_blox(shape_path)

    def getMove(self, board):
        return self.strategy(board, self.bloxs, self.id)

    def _add_blox(self, filename):
        blox_id = 0
        with open(filename, "r") as fp:
            element = []
            val = 0
            for line in fp:
                if line.count("0") + line.count("1") + line.count("\n") != len(
                        line):
                    raise RuntimeError("Invalid block shapes file.")
                if line[0] == "\n":
                    self.bloxs.append(Blox(element, val, blox_id))
                    self.value += val
                    blox_id += 1
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
                self.bloxs.append(Blox(element, val, blox_id))
                self.value += val
                blox_id += 1

    def get_blox(self, id):
        return _resolve(self.bloxs, "id", id)

    def show(self):
        s = ""
        for b in self.bloxs:
            s += b.show()
        return "Player {}\n".format(self.name) + "Hand value: {}\n".format(
            self.value)

    def put(self, id):
        blox = self.get_blox(id)
        self.bloxs.remove(blox)
        self.value -= blox.value
        self.last_value = blox.value
        return blox

    def get_back(self, blox):
        self.bloxs.append(blox)
        self.value += blox.value
        if blox.flipped:
            blox.flip()
        blox.rotate(4 - blox.rotated)

    def calculate_score(self):
        self.score = -1 * self.value
        if self.score == 0:
            self.score = 15
            if self.last_value == 1:
                self.score += 5


class Blox():
    def __init__(self, shape, value, id):
        self.body = np.array(shape)
        self.value = value
        self.id = id
        self.flipped = False
        self.rotated = 0

    def show(self):
        s = ""
        for row in self.body:
            s += "".join(str(int(i)) for i in row) + "\n"
        return "Id: {} Value: {}:\n".format(self.id, self.value) + s + "\n"

    def rotate(self, rotates=1):
        for i in range(rotates):
            self.body = np.rot90(self.body)
        self.rotated = (self.rotated + rotates) % 4

    def flip(self):
        self.body = np.fliplr(self.body)
        self.flip = not self.flip


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
            print(blox.show())
            print(self.show())
            print(x, y)
            raise RuntimeError("Illegal move")
        else:
            self._place(self.board, blox, x, y)
            self.moves_count += 1

    def _place(self, board, blox, x, y):
        for index, val in np.ndenumerate(blox.body):
            if val > 0:
                board[x + index[0]][y + index[1]] = val

    def remove_blox(self, blox, x, y):
        for index, val in np.ndenumerate(blox.body):
            if val > 0:
                self.board[x + index[0]][y + index[1]] = 0
        self.moves_count -= 1

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
            if not (self._covers_field(blox, x, y, 4, 4) or
                    self._covers_field(blox, x, y, 9, 9)):
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


def _resolve(list, attribute, value):
    for item in list:
        if getattr(item, attribute) == value:
            return item
            break

    raise RuntimeError("Non-existing attribute value.")
