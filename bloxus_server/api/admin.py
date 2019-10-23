from django.contrib import admin
from .models import Game, WaitingGame


class GameAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Game._meta.get_fields()]
    readonly_fields = ("last_active",)


admin.site.register(Game, GameAdmin)
admin.site.register(WaitingGame)
