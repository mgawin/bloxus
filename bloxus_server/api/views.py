from django.http import HttpResponseBadRequest, JsonResponse
from bloxus_lib import bloxusgame as bg
from .models import Game, WaitingGame
import dill
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db import transaction
import ast


@csrf_exempt
def init(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()
    name = request.POST.get('Name')
    with transaction.atomic():
        wg = WaitingGame.objects.select_for_update().get(id=1)
        if wg.gid == "0000":
            if name is None:
                name = "Player A"
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
            if name is None:
                name = "Player B"
            player = bg.Player(name, 2)
            game.add_player(player)
            gid = wg.gid
            wg.gid = "0000"
            wg.save()
            ser_game.persisted_game = dill.dumps(game).hex()
            ser_game.save()
    return JsonResponse({"gid": gid, "player": player.input_for_JSON()})


@csrf_exempt
def get(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()
    gid = request.GET.get('gid')
    print(gid)
    ser_game = get_object_or_404(Game, pk=gid)
    game = dill.loads(bytes.fromhex(ser_game.persisted_game))
    return JsonResponse({"status": game.state})


@csrf_exempt
def check_move(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()
    gid = request.POST.get('gid')
    ser_game = get_object_or_404(Game, pk=gid)
    pid = request.POST.get('pid')
    move = ast.literal_eval(request.POST.get('mov'))
    game = dill.loads(bytes.fromhex(ser_game.persisted_game))
    res = game.is_allowed(game.get_player(int(pid)), move)
    return JsonResponse({"allowed": res})


@csrf_exempt
def move(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()
    gid = request.POST.get('gid')
    ser_game = get_object_or_404(Game, pk=gid)
    pid = request.POST.get('pid')
    move = ast.literal_eval(request.POST.get('mov'))
    game = dill.loads(bytes.fromhex(ser_game.persisted_game))
    game.move(game.get_player(int(pid)), move)
    ser_game.persisted_game = dill.dumps(game).hex()
    ser_game.save()
    return JsonResponse({"status": game.state})
