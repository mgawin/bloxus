
import bloxusgame as bg
import bloxusdb as db


def replay_game(id):
    game = bg.Game(
        bg.Player("A", 1),
        bg.Player("B", 2))
    moves = db.get_moves(id)

    i = 0
    k = "a"
    while k and i < len(moves):
        if k == "b":
            if game.undo_move():
                i -= 1
        else:
            move = moves[i]
            game.move(game.get_player(move["player"]), move)
            i += 1
        print(game.show())
        k = input("press key")


replay_game('2d568e32e37748dc95c83de0c9fa107d')
