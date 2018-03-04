import unittest

import bloxusgame as bg


class TestStringMethods(unittest.TestCase):
    def test_invalid_move_touching_side(self):
        self.game = bg.Game(bg.Player("A", 1), bg.Player("B", 2))
        self.game.move(self.game.playerA, {
            "index": 3,
            "x": 3,
            "y": 4,
            "rotates": 1,
            "flip": False
        })
        self.game.move(self.game.playerB, {
            "index": 1,
            "x": 9,
            "y": 9,
            "rotates": 0,
            "flip": False
        })
        self.assertRaises(
            RuntimeError,
            lambda: self.game.move(
                self.game.playerA, {"index": 4, "x": 9, "y": 7, "rotates": 0,
                                    "flip": False})
        )

    def test_invalid_move_initial_field(self):
        self.game = bg.Game(bg.Player("A", 1), bg.Player("B", 2))
        self.game.move(self.game.playerA, {
            "index": 1,
            "x": 4,
            "y": 4,
            "rotates": 0,
            "flip": False
        })
        self.assertRaises(
            RuntimeError,
            lambda: self.game.move(
                self.game.playerB, {"index": 1, "x": 1, "y": 1, "rotates": 0,
                                    "flip": False})
        )

    def test_succesful_moves_sequence_and_game_show(self):
        self.game = bg.Game(bg.Player("A", 1), bg.Player("B", 2))
        self.game.move(self.game.playerA, {
            "index": 0,
            "x": 4,
            "y": 4,
            "rotates": 0,
            "flip": False
        })
        self.game.move(self.game.playerB, {
            "index": 7,
            "x": 8,
            "y": 8,
            "rotates": 0,
            "flip": False
        })
        self.game.move(self.game.playerA, {
            "index": 9,
            "x": 5,
            "y": 5,
            "rotates": 3,
            "flip": True,
        })
        self.game.move(self.game.playerB, {
            "index": 9,
            "x": 10,
            "y": 4,
            "rotates": 0,
            "flip": True
        })
        self.game.move(self.game.playerA, {
            "index": 6,
            "x": 9,
            "y": 4,
            "rotates": 0,
            "flip": False
        })
        self.game.move(self.game.playerB, {
            "index": 12,
            "x": 4,
            "y": 7,
            "rotates": 1,
            "flip": False
        })
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
        self.game.move(self.game.playerA, {
            "index": 3,
            "x": 3,
            "y": 4,
            "rotates": 11,
            "flip": False
        })
        self.game.move(self.game.playerB, {
            "index": 1,
            "x": 9,
            "y": 9,
            "rotates": 0,
            "flip": False
        })

        self.assertRaises(
            PermissionError,
            lambda: self.game.move(
                self.game.playerB, {"index": 4, "x": 9, "y": 7, "rotates": 0,
                                    "flip": False})
        )

    def test_invalid_move_touching_self2(self):
        self.game = bg.Game(bg.Player("A", 1), bg.Player("B", 2))
        self.game.move(self.game.playerA, {
            "index": 4,
            "x": 4,
            "y": 4,
            "rotates": 0,
            "flip": False
        })
        self.game.move(self.game.playerB, {
            "index": 6,
            "x": 8,
            "y": 9,
            "rotates": 0,
            "flip": False
        })
        self.assertRaises(
            RuntimeError,
            lambda: self.game.move(
                self.game.playerA, {"index": 2, "x": 3, "y": 5, "rotates": 0,
                                    "flip": False})
        )

    def test_invalid_move_touching_self3(self):
        self.game = bg.Game(bg.Player("A", 1), bg.Player("B", 2))
        self.game.move(self.game.playerA, {
            "index": 6,
            "x": 3,
            "y": 2,
            "rotates": 0,
            "flip": False
        })
        self.game.move(self.game.playerB, {
            "index": 6,
            "x": 8,
            "y": 9,
            "rotates": 0,
            "flip": False
        })
        self.game.move(self.game.playerA, {
            "index": 0,
            "x": 2,
            "y": 2,
            "rotates": 0,
            "flip": False
        })
        self.game.move(self.game.playerB, {
            "index": 0,
            "x": 7,
            "y": 9,
            "rotates": 0,
            "flip": False
        })
        self.game.move(self.game.playerA, {
            "index": 3,
            "x": 1,
            "y": 3,
            "rotates": 0,
            "flip": False
        })
        self.game.move(self.game.playerB, {
            "index": 3,
            "x": 6,
            "y": 5,
            "rotates": 0,
            "flip": False
        })
        self.game.playerA.flip(8)
        self.assertRaises(
            RuntimeError,
            lambda: self.game.move(
                self.game.playerA, {"index": 8, "x": 1, "y": 4, "rotates": 0,
                                    "flip": False})
        )
