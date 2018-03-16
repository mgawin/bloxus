from django.http import HttpResponseBadRequest, JsonResponse
from bloxus_lib import bloxusgame as bg
from .models import Game, WaitingGame
import dill
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db import transaction


@csrf_exempt
def init(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()
    with transaction.atomic():
        wg = WaitingGame.objects.select_for_update().get(id=1)
        if wg.gid == "0000":
            game = bg.Game(bg.Player("A", 1))
            wg.gid = game.id
            gid = game.id
            pid = 1
            wg.save()
            ser_game = Game()
            ser_game.id = game.id
            ser_game.persisted_game = dill.dumps(game).hex()
            ser_game.save()
        else:
            ser_game = get_object_or_404(Game, pk=wg.gid)
            game = dill.loads(bytes.fromhex(ser_game.persisted_game))
            game.add_player(bg.Player("B", 2))
            gid = wg.gid
            wg.gid = "0000"
            wg.save()
            pid = 2
            ser_game.persisted_game = dill.dumps(game).hex()
            ser_game.save()
    return JsonResponse({"gid": gid, "pid": pid})


@csrf_exempt
def get(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()
    id = request.GET.get('id')
    ser_game = get_object_or_404(Game, pk=id)
    game = dill.loads(bytes.fromhex(ser_game.persisted_game))
    return JsonResponse({"status": game.state})
