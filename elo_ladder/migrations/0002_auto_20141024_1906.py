# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elo_ladder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='losers_new_elo',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='losers_prev_elo',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='winners_new_elo',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='winners_prev_elo',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
