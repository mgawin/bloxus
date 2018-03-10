import bloxusgame as bg
import bloxusdb as db


def replay_game(id):
    game = bg.Game(
        bg.Player("A", 1),
        bg.Player("B", 2))
    moves = db.get_moves(id)

    for move in moves:
        game.move(game.get_player(move["player"]), move)
        print(game.show())
        input("press key")


replay_game('2d568e32e37748dc95c83de0c9fa107d')
