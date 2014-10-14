# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('add_date', models.DateTimeField(verbose_name=b'date added')),
                ('games_played', models.IntegerField(default=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('game_wins', models.IntegerField(default=0)),
                ('game_losses', models.IntegerField(default=0)),
                ('match_wins', models.IntegerField(default=0)),
                ('match_losses', models.IntegerField(default=0)),
                ('elo', models.IntegerField(default=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='match',
            name='losing_player',
            field=models.ForeignKey(related_name=b'match_losing_player', to='elo_ladder.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='winning_player',
            field=models.ForeignKey(related_name=b'match_winning_player', to='elo_ladder.Player'),
            preserve_default=True,
        ),
    ]
