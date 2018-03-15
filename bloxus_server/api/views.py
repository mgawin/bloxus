from django.http import HttpResponseBadRequest, JsonResponse
import bloxus_lib.bloxusgame as bg
import bloxus_lib.bloxus_strategies as strat
from .models import Game
import dill

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404


@csrf_exempt
def init(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()
    game = bg.Game(bg.Player("A", 1, strat.random_bvalue_strategy_with_rotates),
                   bg.Player("B", 2, strat.random_bvalue_strategy))
    ser_game = Game()
    ser_game.id = game.id
    ser_game.persisted_game = dill.dumps(game).hex()
    print(type(ser_game.persisted_game))
    ser_game.save()
    return JsonResponse({"id": game.id})


@csrf_exempt
def get(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()
    id = request.GET.get('id')
    ser_game = get_object_or_404(Game, pk=id)

    game = dill.loads(bytes.fromhex(ser_game.persisted_game))

    return JsonResponse({"board": game.board.show()})
