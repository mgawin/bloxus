from tinydb import TinyDB


def store_game(game):
    db = TinyDB("./database/game_stats.json", create_dirs=True)
    record = {"game": game.id}
    record["playerA"] = {"strategy": game.playerA.strategy.__name__}
    record["playerB"] = {"strategy": game.playerB.strategy.__name__}

    record["playerA"]["name"] = game.playerA.name
    record["playerB"]["name"] = game.playerB.name

    db.insert(record)
    db.close()


def get_games_stats():
    db = TinyDB("./database/game_stats.json", create_dirs=True)
    games = db.all()
    db.close()
    return len(games)
