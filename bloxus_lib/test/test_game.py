import unittest

import bloxusgame as bg


class TestStringMethods(unittest.TestCase):
    def test_invalid_move_touching_side(self):
        self.game = bg.Game(bg.Player("A", 1), bg.Player("B", 2))
        self.game.move(self.game.playerA, {
            "id": 3,
            "x": 3,
            "y": 4,
            "rotates": 1,
            "flip": False
        })
        self.game.move(self.game.playerB, {
            "id": 1,
            "x": 9,
            "y": 9,
            "rotates": 0,
            "flip": False
        })
        self.assertRaises(
            RuntimeError,
            lambda: self.game.move(
                self.game.playerA, {"id": 4, "x": 9, "y": 7, "rotates": 0,
                                    "flip": False})
        )

    def test_invalid_move_initial_field(self):
        self.game = bg.Game(bg.Player("A", 1), bg.Player("B", 2))
        self.game.move(self.game.playerA, {
            "id": 1,
            "x": 4,
            "y": 4,
            "rotates": 0,
            "flip": False
        })
        self.assertRaises(
            RuntimeError,
            lambda: self.game.move(
                self.game.playerB, {"id": 1, "x": 1, "y": 1, "rotates": 0,
                                    "flip": False})
        )

    def test_succesful_moves_sequence_and_game_show(self):
        self.game = bg.Game(bg.Player("A", 1), bg.Player("B", 2))
        self.game.move(self.game.playerA, {
            "id": 0,
            "x": 4,
            "y": 4,
            "rotates": 0,
            "flip": False
        })
        self.game.move(self.game.playerB, {
            "id": 7,
            "x": 8,
            "y": 8,
            "rotates": 0,
            "flip": False
        })
        self.game.move(self.game.playerA, {
            "id": 10,
            "x": 5,
            "y": 5,
            "rotates": 3,
            "flip": True,
        })
        self.game.move(self.game.playerB, {
            "id": 10,
            "x": 10,
            "y": 4,
            "rotates": 0,
            "flip": True
        })
        self.game.move(self.game.playerA, {
            "id": 7,
            "x": 9,
            "y": 4,
            "rotates": 0,
            "flip": False
        })
        self.game.move(self.game.playerB, {
            "id": 14,
            "x": 4,
            "y": 7,
            "rotates": 1,
            "flip": False
        })
        self.assertMultiLineEqual(self.game.board.show(), '''00000000000000
00000000000000
00000000000000
00000000000000
00001002000000
00000112200000
00000012000000
00000012000000
00000010220000
00001100220000
00001102000000
00002222000000
00000000000000
00000000000000
''')

    def test_wrong_turn_order(self):
        self.game = bg.Game(bg.Player("A", 1), bg.Player("B", 2))
        self.game.move(self.game.playerA, {
            "id": 3,
            "x": 3,
            "y": 4,
            "rotates": 11,
            "flip": False
        })
        self.game.move(self.game.playerB, {
            "id": 1,
            "x": 9,
            "y": 9,
            "rotates": 0,
            "flip": False
        })

        self.assertRaises(
            PermissionError,
            lambda: self.game.move(
                self.game.playerB, {"id": 4, "x": 9, "y": 7, "rotates": 0,
                                    "flip": False})
        )

    def test_invalid_move_touching_self2(self):
        self.game = bg.Game(bg.Player("A", 1), bg.Player("B", 2))
        self.game.move(self.game.playerA, {
            "id": 4,
            "x": 4,
            "y": 4,
            "rotates": 0,
            "flip": False
        })
        self.game.move(self.game.playerB, {
            "id": 6,
            "x": 8,
            "y": 9,
            "rotates": 0,
            "flip": False
        })
        self.assertRaises(
            RuntimeError,
            lambda: self.game.move(
                self.game.playerA, {"id": 2, "x": 3, "y": 5, "rotates": 0,
                                    "flip": False})
        )

    def test_invalid_move_touching_self3(self):
        self.game = bg.Game(bg.Player("A", 1), bg.Player("B", 2))
        self.game.move(self.game.playerA, {
            "id": 6,
            "x": 3,
            "y": 2,
            "rotates": 0,
            "flip": False
        })
        self.game.move(self.game.playerB, {
            "id": 6,
            "x": 8,
            "y": 9,
            "rotates": 0,
            "flip": False
        })
        self.game.move(self.game.playerA, {
            "id": 0,
            "x": 2,
            "y": 2,
            "rotates": 0,
            "flip": False
        })
        self.game.move(self.game.playerB, {
            "id": 0,
            "x": 7,
            "y": 9,
            "rotates": 0,
            "flip": False
        })
        self.game.move(self.game.playerA, {
            "id": 4,
            "x": 1,
            "y": 3,
            "rotates": 0,
            "flip": False
        })
        self.game.move(self.game.playerB, {
            "id": 4,
            "x": 6,
            "y": 5,
            "rotates": 0,
            "flip": False
        })
        self.assertRaises(
            RuntimeError,
            lambda: self.game.move(
                self.game.playerA, {"id": 11, "x": 1, "y": 4, "rotates": 0,
                                    "flip": False})
        )
