import random

import numpy as np


def simple_strategy(board, bloxs, id):
    selected_moves = _get_available_moves(board, bloxs)
    if len(selected_moves) > 0:
        return selected_moves[0]
    else:
        return None


def random_strategy(board, bloxs, id):
    selected_moves = _get_available_moves(board, bloxs)
    if len(selected_moves) > 0:
        return selected_moves[random.randrange(len(selected_moves))]
    else:
        return None


def _get_available_moves(board, bloxs):
    available_moves = []
    for ix, blox in enumerate(bloxs):
        for x in range(13):
            for y in range(13):
                if board._is_allowed(blox, x, y):
                    available_moves.append({
                        "blox": blox,
                        "x": x,
                        "y": y,
                        "index": ix
                    })
    return available_moves
