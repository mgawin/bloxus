import unittest

import bloxus_lib.bloxusgame as bg


class TestStringMethods(unittest.TestCase):
    def test_board_move_adjacent_corner(self):
        b = bg.Board()
        b.moves_count = 3
        player = bg.Player("Name", 1)
        b.board[2][0] = 2
        b.board[2][1] = 2
        b.board[3][0] = 2
        b.board[4][0] = 2
        b.board[5][0] = 2
        b.board[1][3] = 1
        b.board[1][4] = 1
        b.board[1][5] = 1
        b.board[1][6] = 1
        b.board[1][7] = 1
        b.board[2][2] = 1
        b.board[3][1] = 1
        b.board[3][2] = 1
        b.board[3][3] = 1
        b.board[4][2] = 1
        print(b.show())
        blox = player.get_blox(3)
        self.assertTrue(b._is_allowed(blox, 0, 0))

    def test_board_move_block_on_border(self):
        b = bg.Board()
        b.moves_count = 3
        player = bg.Player("Name", 1)
        b.board[10][8] = 1
        b.board[10][9] = 1
        b.board[10][10] = 1
        print(b.show())
        blox = player.get_blox(16)
        print(blox.show())
        self.assertTrue(b._is_allowed(blox, 11, 7))

    def test_board_move_with_rotations(self):
        b = bg.Board()
        b.moves_count = 3
        player = bg.Player("Name", 1)
        b.board[9][7] = 1
        b.board[9][8] = 1
        b.board[9][9] = 2
        b.board[9][10] = 2
        b.board[9][11] = 2
        b.board[9][12] = 2
        b.board[10][7] = 2
        b.board[10][8] = 2
        b.board[10][11] = 2
        b.board[11][8] = 2
        b.board[11][10] = 2
        b.board[12][7] = 2
        b.board[12][8] = 2
        b.board[12][10] = 2
        b.board[12][11] = 2
        b.board[12][12] = 2
        b.board[13][12] = 2

        print(b.show())
        blox = player.get_blox(10)
        blox.rotate(3)
        print(blox.show())
        self.assertTrue(b._is_allowed(blox, 10, 9))

    def test_board_move_allowed_with_rotations2(self):
        b = bg.Board()
        b.moves_count = 3
        player = bg.Player("Name", 1)
        b.board[6][8] = 1
        b.board[7][8] = 1
        b.board[7][9] = 1
        b.board[7][10] = 1
        b.board[7][11] = 1

        b.board[3][12] = 2
        b.board[4][12] = 2
        b.board[5][12] = 2
        b.board[6][12] = 2
        b.board[7][12] = 2

        b.board[8][9] = 2
        b.board[9][9] = 2
        b.board[9][10] = 2
        b.board[9][11] = 2
        b.board[8][11] = 2

        print(b.show())
        blox = player.get_blox(16)
        blox.rotate(1)
        print(blox.show())
        self.assertTrue(b._is_allowed(blox, 8, 10))

    def test_board_move_allowed_rotation3(self):
        b = bg.Board()
        b.moves_count = 3
        player = bg.Player("Name", 1)
        b.board[6][8] = 1
        b.board[7][8] = 1
        b.board[8][8] = 1
        b.board[9][8] = 1
        b.board[9][7] = 1

        b.board[6][9] = 2
        b.board[7][9] = 2
        b.board[8][9] = 2
        b.board[9][9] = 2
        b.board[10][9] = 2

        b.board[8][11] = 2
        b.board[9][11] = 2
        b.board[10][11] = 2
        b.board[11][11] = 2
        b.board[11][10] = 2

        print(b.show())
        blox = player.get_blox(16)
        blox.rotate(2)
        print(blox.show())
        self.assertTrue(b._is_allowed(blox, 5, 9))

    def test_board_move_not_allowed_touching_side(self):
        b = bg.Board()
        b.moves_count = 3
        player = bg.Player("Name", 1)
        b.board[0][2] = 1
        b.board[1][0] = 1
        b.board[1][1] = 1
        b.board[1][2] = 1
        b.board[2][2] = 1

        b.board[3][3] = 1
        b.board[4][2] = 1
        b.board[4][3] = 1
        b.board[4][4] = 1

        b.board[3][5] = 1
        b.board[3][6] = 1
        b.board[3][7] = 1

        print(b.show())
        blox = player.get_blox(13)
        print(blox.show())
        self.assertFalse(b._is_allowed(blox, 1, 4))
