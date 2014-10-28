# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elo_ladder', '0003_auto_20141024_2031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='game_win_percent',
        ),
        migrations.RemoveField(
            model_name='player',
            name='match_win_percent',
        ),
    ]
