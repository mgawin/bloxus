from tinydb import TinyDB, where


def store_game(game):
    db = TinyDB("./database/game_stats.json", create_dirs=True)
    record = {"game": game.id}
    record["playerA"] = {"strategy": game.playerA.strategy.__name__}
    record["playerB"] = {"strategy": game.playerB.strategy.__name__}

    record["playerA"]["name"] = game.playerA.name
    record["playerB"]["name"] = game.playerB.name

    record["playerA"]["score"] = game.playerA.score
    record["playerB"]["score"] = game.playerB.score
    if game.playerA.score > game.playerB.score:
        record["playerA"]["win"] = "Y"
        record["playerB"]["win"] = "N"

    elif game.playerB.score > game.playerA.score:
        record["playerA"]["win"] = "N"
        record["playerB"]["win"] = "Y"
    else:
        record["playerA"]["win"] = "Y"
        record["playerB"]["win"] = "Y"

    db.insert(record)
    db.close()


def store_move(id, move):
    move['gameId'] = id
    db = TinyDB("./database/game_moves.json", create_dirs=True)
    db.insert(move)
    db.close()


def get_strategy_win_stats(strat):
    db = TinyDB("./database/game_stats.json", create_dirs=False)
    games = db.search(where("playerB").strategy == strat)

    games += db.search(where("playerA").strategy == strat)
    win = 0
    for game in games:
        if (game["playerA"]["win"] == "Y" and
            game["playerA"]["strategy"] == strat) or \
            (game["playerB"]["win"] == "Y" and
             game["playerB"]["strategy"] == strat):
            win += 1

    if len(games) > 0:
        win_rate = win / len(games) * 100
    else:
        win_rate = 0

    print("Strategy {}:\nWins rate: {:6.2f}%".format(strat, win_rate))

    db.close()


def get_moves(id):
    db = TinyDB("./database/game_moves.json", create_dirs=False)
    games = db.search(where("gameId") == id)
    return games
