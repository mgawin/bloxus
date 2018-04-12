import uuid
import numpy as np
from bloxus_lib import bloxusdb as db
import os.path
from enum import IntEnum
import copy


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

    def __init__(self, playerA=None, playerB=None):
        self.board = Board()
        self.state = GameState.WAITING
        self.playerA = playerA
        self.playerB = playerB
        self.id = str(uuid.uuid4()).replace("-", "")
        self.game_end = 0
        self.move_history = []
        self.move_history_len = 40
        if (playerA and playerB) is not None:
            self.state = GameState.PLAYER_A

    def add_player(self, player):
        if self.state != GameState.WAITING:
            raise RuntimeError("Invalid action. Game in progress!")
        if self.playerA is None:
            self.playerA = player
        else:
            self.playerB = player
        if (self.playerA and self.playerB) is not None:
            self.state = GameState.PLAYER_A

    def get_last_move(self):
        last_move = {}
        if self.move_history[0] is not None:
            last_move["blox"] = self.move_history[0]["blox"].input_for_JSON()
            last_move["pid"] = self.move_history[0]["player_id"]
            last_move["x"] = self.move_history[0]["x"]
            last_move["y"] = self.move_history[0]["y"]
        return last_move

    def get_player(self, id):
        if self.playerA.id == id:
            return self.playerA
        if self.playerB is not None:
            if self.playerB.id == id:
                return self.playerB
        else:
            raise RuntimeError("Non-existing player id value.")

    def move(self, player, move=None):
        if (self.state != GameState.PLAYER_A) and (self.state != GameState.PLAYER_B):
            raise RuntimeError("Invalid action. Game not in progress.")
        if move is None:
            move = player.getMove(self.board)
        if move:
            id, x, y, rotates, flip = move["id"], move["x"], move[
                "y"], move["rotates"], move["flip"]
            blox = player.put(id)
            if blox is None:
                raise RuntimeError("Non-existing blox id value.")
            if int(rotates) > 0:
                blox.rotate(int(rotates))
            if int(flip) > 0:
                blox.flip()
            self.game_end = 0
        else:
            self.game_end += 1
            if self.game_end > 3:
                self.state = GameState.FINISHED
                self.playerA.calculate_score()
                self.playerB.calculate_score()
                db.store_game(self)
            return
        correct_order = False
        if self.state == GameState.PLAYER_A and player is self.playerA:
            correct_order = True
        if self.state == GameState.PLAYER_B and player is self.playerB:
            correct_order = True
        if correct_order:
            self.board.place_blox(blox, x, y)
            if self.state == GameState.PLAYER_A:
                self.state = GameState.PLAYER_B
            elif self.state == GameState.PLAYER_B:
                self.state = GameState.PLAYER_A
            move['player'] = player.id
            db.store_move(self.id, move)
            self._add_to_history(
                {"player_id": player.id, "blox": blox, "x": x, "y": y})
        else:
            raise PermissionError("Wrong turn order!")

    def undo_move(self):
        if (self.state != GameState.PLAYER_A) and (self.state != GameState.PLAYER_B):
            raise RuntimeError("Invalid action. Game not in progress.")
        if len(self.move_history) > 0:
            move = self.move_history[0]
            player = self.get_player(move["player_id"])
            blox = move["blox"]
            x = move["x"]
            y = move["y"]
            self.board.remove_blox(blox, x, y)
            del self.move_history[0]
            player.get_back(blox)
            if self.state == GameState.PLAYER_A:
                self.state = GameState.PLAYER_B
            elif self.state == GameState.PLAYER_B:
                self.state = GameState.PLAYER_A
            return True

        return False

    def is_allowed(self, player, move):
        id, x, y, rotates, flip = move["id"], move["x"], move["y"], move["rotates"], move["flip"]
        blox = player.get_blox(id)
        if blox is None:
            return False
        if int(rotates) > 0:
            blox.rotate(int(rotates))
        if int(flip) > 0:
            blox.flip()
        return self.board._is_allowed(blox, x, y)

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

    def input_for_JSON(self):
        obj = {"name": self.name, "pid": self.id}
        bloxs_obj = []
        for blox in self.bloxs:
            bloxs_obj.append(blox.input_for_JSON())
        obj["bloxs"] = bloxs_obj
        return obj

    def put(self, id):
        blox = self.get_blox(id)
        if blox is not None:
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

    def input_for_JSON(self):
        shape = []
        for row in self.body:
            shape.append([int(i) for i in row])
        return {'shp': shape, 'bid': self.id}

    def rotate(self, rotates=1):
        for i in range(rotates):
            self.body = np.rot90(self.body)
        self.rotated = (self.rotated + rotates) % 4

    def flip(self):
        self.body = np.fliplr(self.body)
        self.flip = not self.flip


class Board():
    def __init__(self):
        self.board = np.zeros((14, 14))
        self.moves_count = 0

    def show(self):
        s = ""
        for row in self.board:
            s += ("".join(str(int(i)) for i in row)) + "\n"
        return s

    def input_for_JSON(self):
        return self.board.tolist()

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

    def get_available_moves(self, blox, rotates, flip):
        available_moves = []
        temp_blox = copy.deepcopy(blox)
        for k in range(rotates):
            temp_blox.rotate()
        if flip > 0:
            temp_blox.flip()
        for x in range(14):
            for y in range(14):
                if self._is_allowed(temp_blox, x, y):
                    available_moves.append([x, y])
        return available_moves

    def _is_allowed(self, blox, x, y):
        lx, ly = np.shape(blox.body)
        if (x + lx > 14) or (y + ly > 14):
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
        vboard[1:15, 1:15] = self.board
        x = x + 1
        y = y + 1
        self._place(vboard, blox, x, y)
        for index, val in np.ndenumerate(blox.body):
            if val > 0:
                if vboard[x + index[0] - 1][y + index[1] - 1] == val and \
                        vboard[x + index[0] - 1][y + index[1]] != val and \
                        vboard[x + index[0]][y + index[1] - 1] != val:
                    return True
                if vboard[x + index[0] + 1][y + index[1] - 1] == val and \
                        vboard[x + index[0]][y + index[1] - 1] != val and \
                        vboard[x + index[0] + 1][y + index[1]] != val:
                    return True
                if vboard[x + index[0] - 1][y + index[1] + 1] == val and \
                        vboard[x + index[0] - 1][y + index[1]] != val and \
                        vboard[x + index[0]][y + index[1] + 1] != val:
                    return True
                if vboard[x + index[0] + 1][y + index[1] + 1] == val and \
                        vboard[x + index[0]][y + index[1] + 1] != val and \
                        vboard[x + index[0] + 1][y + index[1]] != val:
                    return True
        return False

    def _is_adjacent_own_side(self, blox, x, y):
        if self.moves_count < 2:
            return False
        vboard = np.zeros((16, 16))
        vboard[1:15, 1:15] = self.board
        x = x + 1
        y = y + 1
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

    return None


class GameState(IntEnum):
    WAITING = 1
    PLAYER_A = 2
    PLAYER_B = 3
    FINISHED = 4
