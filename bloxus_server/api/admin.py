from django.contrib import admin
from .models import Game, WaitingGame

admin.site.register(Game)
admin.site.register(WaitingGame)
