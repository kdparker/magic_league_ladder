from django.contrib import admin
from elo_ladder.models import Player, Match

# Register your models here.
admin.site.register(Player)
admin.site.register(Match)