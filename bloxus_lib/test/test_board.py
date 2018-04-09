import unittest

import bloxusgame as bg


class TestStringMethods(unittest.TestCase):
    def test_board_move_adjacent_corner(self):
        b = bg.Board()
        b.moves_count = 3
        player = bg.Player('Name', 1)
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
        player = bg.Player('Name', 1)
        b.board[10][8] = 1
        b.board[10][9] = 1
        b.board[10][10] = 1
        print(b.show())
        blox = player.get_blox(16)
        print(blox.show())
        self.assertTrue(b._is_allowed(blox, 11, 7))
