from django.http import HttpResponseBadRequest, JsonResponse
from bloxus_lib import bloxusgame as bg
from bloxus_lib import bloxus_strategies as strat
from .models import Game, WaitingGame
import dill
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db import transaction
import time
import ast


@csrf_exempt
def init(request):
    if not _verify_request_params(request, ["name"], "POST"):
        return HttpResponseBadRequest()
    name = request.POST.get("name")
    if request.POST.get("auto") is not None:
        player = bg.Player(name, 1)
        robot_player = bg.Player("Robot", 2, strat.random_bvalue_strategy_with_rotates)
        game = bg.Game(player, robot_player)
        ser_game = Game()
        ser_game.id = game.id
        ser_game.robot_game = True
        gid = game.id
        ser_game.persisted_game = dill.dumps(game).hex()
        ser_game.save()

    else:
        with transaction.atomic():
            wg = WaitingGame.objects.select_for_update().get()
            if wg.gid == "0000":
                player = bg.Player(name, 1)
                game = bg.Game(player)
                wg.gid = game.id
                gid = game.id
                wg.save()
                ser_game = Game()
                ser_game.id = game.id
                ser_game.persisted_game = dill.dumps(game).hex()
                ser_game.save()
            else:
                ser_game = get_object_or_404(Game, pk=wg.gid)
                game = dill.loads(bytes.fromhex(ser_game.persisted_game))
                player = bg.Player(name, 2)
                game.add_player(player)
                gid = wg.gid
                wg.gid = "0000"
                wg.save()
                ser_game.persisted_game = dill.dumps(game).hex()
                ser_game.save()
    return JsonResponse(
        {"gid": gid, "status": game.state, "player": player.input_for_JSON()}
    )


@csrf_exempt
def get(request):
    if not _verify_request_params(request, ["gid"], "GET"):
        return HttpResponseBadRequest()
    gid = request.GET.get("gid")
    ser_game = get_object_or_404(Game, pk=gid)
    game = dill.loads(bytes.fromhex(ser_game.persisted_game))
    last_move = game.get_last_move()
    return JsonResponse(
        {
            "status": game.state,
            "result": game.get_game_result_for_JSON(),
            "last": last_move,
        }
    )


@csrf_exempt
def check_move(request):
    if not _verify_request_params(request, ["gid", "pid", "mov"], "POST"):
        return HttpResponseBadRequest()
    gid = request.POST.get("gid")
    ser_game = get_object_or_404(Game, pk=gid)
    pid = request.POST.get("pid")
    move = ast.literal_eval(request.POST.get("mov"))
    game = dill.loads(bytes.fromhex(ser_game.persisted_game))
    res = game.is_allowed(game.get_player(int(pid)), move)
    return JsonResponse({"allowed": res})


@csrf_exempt
def move(request):
    if not _verify_request_params(request, ["gid", "pid", "mov"], "POST"):
        return HttpResponseBadRequest()
    gid = request.POST.get("gid")
    ser_game = get_object_or_404(Game, pk=gid)
    pid = request.POST.get("pid")
    move = ast.literal_eval(request.POST.get("mov"))
    if move["id"] is None:
        move = None

    game = dill.loads(bytes.fromhex(ser_game.persisted_game))
    try:
        game.move(game.get_player(int(pid)), move)
        print(game.state)
        ser_game.persisted_game = dill.dumps(game).hex()
        ser_game.save()
    except RuntimeError as e:
        print(str(e))
        return HttpResponseBadRequest()
    last_move = ""
    if ser_game.robot_game:
        try:
            game.move(game.get_player(2))
            last_move = game.get_last_move()
        except RuntimeError:
            return HttpResponseBadRequest()

    ser_game.persisted_game = dill.dumps(game).hex()
    time.sleep(0)
    ser_game.save()

    return JsonResponse(
        {
            "status": game.state,
            "board": game.board.input_for_JSON(),
            "last": last_move,
            "result": game.get_game_result_for_JSON(),
        }
    )


@csrf_exempt
def get_available_moves(request):
    if not _verify_request_params(
        request, ["gid", "pid", "bid", "rotates", "flip"], "POST"
    ):
        return HttpResponseBadRequest()
    gid = request.POST.get("gid")
    ser_game = get_object_or_404(Game, pk=gid)
    pid = request.POST.get("pid")
    bid = request.POST.get("bid")
    flip = request.POST.get("flip")
    rotates = request.POST.get("rotates")
    game = dill.loads(bytes.fromhex(ser_game.persisted_game))

    moves = game.board.get_available_moves(
        game.get_player(int(pid)).get_blox(int(bid)), int(rotates), int(flip)
    )
    return JsonResponse({"moves": moves})


def _verify_request_params(request, params, method):
    if request.method != method:
        return False
    if method == "POST":
        data = request.POST
    elif method == "GET":
        data = request.GET
    for param in params:
        if param not in data:
            return False
        else:
            if data.get(param) is None or data.get(param) == "":
                return False
    return True
