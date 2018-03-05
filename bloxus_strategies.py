import random
import copy


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


def random_bvalue_strategy(board, bloxs, id):
    selected_moves = _get_available_moves(board, bloxs)
    if len(selected_moves) > 0:
        i = max(
            range(len(selected_moves)),
            key=lambda index: selected_moves[index]['blox'].value)
        del selected_moves[i]['blox']
        return selected_moves[i]
    else:
        return None


def random_minval_strategy(board, bloxs, id):
    selected_moves = _get_available_moves(board, bloxs)
    if len(selected_moves) > 0:
        i = min(
            range(len(selected_moves)),
            key=lambda index: selected_moves[index]['blox'].value)
        del selected_moves[i]['blox']
        return selected_moves[i]
    else:
        return None


def random_bvalue_strategy_with_rotates(board, bloxs, id):
    selected_moves = _get_available_moves(board, bloxs, True)
    if len(selected_moves) > 0:
        # i = max(
        #     range(len(selected_moves)),
        #     key=lambda index: selected_moves[index]['blox'].value)
        mx = max(selected_moves,
                 key=lambda elem: elem['blox'].value)
        best_moves = []
        for k in range(len(selected_moves)):
            if selected_moves[k]['blox'].value == mx['blox'].value:
                best_moves.append(selected_moves[k])
        i = random.randrange(len(best_moves))
        del best_moves[i]['blox']
        return best_moves[i]
    else:
        return None


def _get_available_moves(board, bloxs, rotate=False):
    available_moves = []
    for ix, blox in enumerate(bloxs):
        for x in range(13):
            for y in range(13):
                if board._is_allowed(blox, x, y):
                    available_moves.append({
                        "blox": blox,
                        "index": ix,
                        "x": x,
                        "y": y,
                        "rotates": 0,
                        "flip": False
                    })
                if rotate:
                    temp_blox = copy.deepcopy(blox)
                    for k in range(1, 4):
                        temp_blox.rotate()
                        if board._is_allowed(temp_blox, x, y):
                            available_moves.append({
                                "blox": blox,
                                "index": ix,
                                "x": x,
                                "y": y,
                                "rotates": k,
                                "flip": False
                            })

    return available_moves
