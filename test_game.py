import unittest

import bloxusgame as bg

# game = bg.Game()
# game.show()
# game.playerA.rotate(1)
# game.move(game.playerB.put(3), 5, 9)
# game.show()
# game.move(game.playerA.put(1), 9, 6)
# game.show()
# game.move(game.playerA.put(4), 10, 7)
# game.show()


class TestStringMethods(unittest.TestCase):
    def test_invalid_move_touching_side(self):
        self.game = bg.Game()
        self.game.playerA.rotate(1)
        self.game.move(self.game.playerB.put(3), 3, 4)
        self.game.move(self.game.playerA.put(1), 9, 9)

        self.assertRaises(
            RuntimeError,
            lambda: self.game.move(self.game.playerA.put(4), 9, 7))

    def test_invalid_move_initial_field(self):
        self.game = bg.Game()
        self.game.move(self.game.playerA.put(1), 4, 4)
        self.assertRaises(RuntimeError,
                          lambda: self.game.move(self.game.move(self.game.playerB.put(1), 1, 1)
                                                 ))

    def test_succesful_moves_sequence_and_game_show(self):
        self.game = bg.Game()
        self.game.move(self.game.playerA.put(1), 4, 4)
        self.game.move(self.game.playerB.put(4), 8, 8)
        self.game.playerA.rotate(2)
        self.game.move(self.game.playerA.put(2), 5, 5)
        self.game.move(self.game.playerB.put(3), 10, 4)
        self.game.move(self.game.playerA.put(2), 9, 4)
        self.game.playerB.rotate(4)
        self.game.playerB.flip(4)
        self.game.move(self.game.playerB.put(4), 4, 6)
        print(self.game.board.show())
        self.assertMultiLineEqual(self.game.board.show(
        ), '''0000000000000
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


if __name__ == '__main__':
    unittest.main()
