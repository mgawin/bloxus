import unittest

import bloxusgame as bg


class TestStringMethods(unittest.TestCase):
    def test_invalid_move_touching_side(self):
        self.game = bg.Game(bg.Player("A", 1), bg.Player("B", 2))
        self.game.playerA.rotate(1)
        self.game.move(self.game.playerA, self.game.playerA.put(3), 3, 4)
        self.game.move(self.game.playerB, self.game.playerB.put(1), 9, 9)
        self.assertRaises(
            RuntimeError,
            lambda: self.game.move(
                self.game.playerA, self.game.playerA.put(4), 9, 7)
        )

    def test_invalid_move_initial_field(self):
        self.game = bg.Game(bg.Player("A", 1), bg.Player("B", 2))
        self.game.move(self.game.playerA, self.game.playerA.put(1), 4, 4)
        self.assertRaises(
            RuntimeError,
            lambda: self.game.move(
                self.game.playerB, self.game.playerB.put(1), 1, 1)
        )

    def test_succesful_moves_sequence_and_game_show(self):
        self.game = bg.Game(bg.Player("A", 1), bg.Player("B", 2))
        self.game.move(self.game.playerA, self.game.playerA.put(0), 4, 4)
        self.game.move(self.game.playerB, self.game.playerB.put(7), 8, 8)
        self.game.playerA.rotate(9)
        self.game.playerA.rotate(9)
        self.game.playerA.rotate(9)
        self.game.playerA.flip(9)
        self.game.move(self.game.playerA, self.game.playerA.put(9), 5, 5)
        self.game.playerB.flip(9)
        self.game.move(self.game.playerB, self.game.playerB.put(9), 10, 4)
        self.game.move(self.game.playerA, self.game.playerA.put(6), 9, 4)
        self.game.playerB.rotate(12)
        self.game.move(self.game.playerB, self.game.playerB.put(12), 4, 7)
        self.assertMultiLineEqual(self.game.board.show(), '''0000000000000
0000000000000
0000000000000
0000000000000
0000100200000
0000011220000
0000001200000
0000001200000
0000001022000
0000110022000
0000110200000
0000222200000
0000000000000
''')

    def test_wrong_turn_order(self):
        self.game = bg.Game(bg.Player("A", 1), bg.Player("B", 2))
        self.game.playerA.rotate(1)
        self.game.move(self.game.playerA, self.game.playerA.put(3), 3, 4)
        self.game.move(self.game.playerB, self.game.playerB.put(1), 9, 9)

        self.assertRaises(
            PermissionError,
            lambda: self.game.move(
                self.game.playerB, self.game.playerB.put(4), 9, 7)
        )

    def test_invalid_move_touching_self2(self):
        self.game = bg.Game(bg.Player("A", 1), bg.Player("B", 2))
        self.game.move(self.game.playerA, self.game.playerA.put(4), 4, 4)
        self.game.move(self.game.playerB, self.game.playerB.put(6), 8, 9)
        self.game.playerA.flip(9)
        self.assertRaises(
            RuntimeError,
            lambda: self.game.move(
                self.game.playerA, self.game.playerA.put(2), 3, 5)
        )

    def test_invalid_move_touching_self3(self):
        self.game = bg.Game(bg.Player("A", 1), bg.Player("B", 2))
        self.game.move(self.game.playerA, self.game.playerA.put(6), 3, 2)
        self.game.move(self.game.playerB, self.game.playerB.put(6), 8, 9)
        self.game.move(self.game.playerA, self.game.playerA.put(0), 2, 2)
        self.game.move(self.game.playerB, self.game.playerB.put(0), 7, 9)
        self.game.move(self.game.playerA, self.game.playerA.put(3), 1, 3)
        self.game.move(self.game.playerB, self.game.playerB.put(3), 6, 5)
        self.game.playerA.flip(8)
        self.assertRaises(
            RuntimeError,
            lambda: self.game.move(
                self.game.playerA, self.game.playerA.put(8), 1, 4)
        )


unittest.main()
