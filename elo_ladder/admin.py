from django.contrib import admin
from elo_ladder.models import Player, Match, ResetPage

admin.site.register(Player)
admin.site.register(Match)
admin.site.register(ResetPage)