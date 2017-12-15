import random

import numpy as np


def simple_strategy(board, bloxs, id):
    selected_moves = []
    for ix, blox in enumerate(bloxs):
        #    print(blox.show())
        for x in range(13):
            for y in range(13):
                #            print(x, y)
                if board._is_allowed(blox, x, y):
                    selected_moves.append({
                        "blox": blox,
                        "x": x,
                        "y": y,
                        "index": ix
                    })
    if len(selected_moves) > 0:
        print(selected_moves[0])
        return selected_moves[0]
    else:
        return None


def random_strategy(board, bloxs, id):
    selected_moves = []
    for ix, blox in enumerate(bloxs):
        #    print(blox.show())
        for x in range(13):
            for y in range(13):
                #            print(x, y)
                if board._is_allowed(blox, x, y):
                    selected_moves.append({
                        "blox": blox,
                        "x": x,
                        "y": y,
                        "index": ix
                    })
    if len(selected_moves) > 0:
        return selected_moves[random.randrange(len(selected_moves))]
    else:
        return None
