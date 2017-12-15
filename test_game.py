import unittest

import bloxus_strategies as strat
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
        self.game.move(self.game.playerA, self.game.playerA.put(1), 4, 4)
        self.game.move(self.game.playerB, self.game.playerB.put(4), 8, 8)
        self.game.playerA.rotate(2)
        self.game.move(self.game.playerA, self.game.playerA.put(2), 5, 5)
        self.game.move(self.game.playerB, self.game.playerB.put(3), 10, 4)
        self.game.move(self.game.playerA, self.game.playerA.put(2), 9, 4)
        self.game.playerB.rotate(4)
        self.game.playerB.flip(4)
        self.game.move(self.game.playerB, self.game.playerB.put(4), 4, 6)
        self.assertEqual(len(self.game.game_state), 7)
        self.assertMultiLineEqual(self.game.board.show(), '''0000000000000
0000000000000
0000000000000
0000000000000
0000102200000
0000011200000
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
        self.game.move(self.game.playerA, self.game.playerA.put(2), 4, 4)
        self.game.move(self.game.playerB, self.game.playerB.put(0), 8, 9)
        self.assertRaises(
            RuntimeError,
            lambda: self.game.move(
                self.game.playerA, self.game.playerA.put(2), 3, 5)
        )

    def test_invalid_move_touching_self3(self):
        self.game = bg.Game(bg.Player("A", 1), bg.Player("B", 2))
        self.game.move(self.game.playerA, self.game.playerA.put(0), 3, 2)
        self.game.move(self.game.playerB, self.game.playerB.put(0), 8, 9)
        self.game.move(self.game.playerA, self.game.playerA.put(0), 2, 2)
        self.game.move(self.game.playerB, self.game.playerB.put(0), 7, 9)
        self.game.move(self.game.playerA, self.game.playerA.put(0), 1, 3)
        self.game.move(self.game.playerB, self.game.playerB.put(0), 6, 5)
        self.assertRaises(
            RuntimeError,
            lambda: self.game.move(
                self.game.playerA, self.game.playerA.put(0), 1, 4)
        )


unittest.main()
