import bloxus_strategies as strat
import bloxusgame as bg


def run():
    game = bg.Game(
        bg.Player("A", 1, strat.simple_strategy),
        bg.Player("B", 2, strat.random_strategy))
    while not game.finished:
        if game.next_A:
            game.move(game.playerA)
        else:
            game.move(game.playerB)

    print(game.show())
    # input("press key")


if __name__ == '__main__':
    run()
