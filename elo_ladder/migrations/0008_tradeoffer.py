# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elo_ladder', '0007_player_collection'),
    ]

    operations = [
        migrations.CreateModel(
            name='TradeOffer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('offered_cards', models.TextField(default=b'')),
                ('wanted_cards', models.TextField(default=b'')),
                ('recipient', models.ForeignKey(related_name=b'recipient', default=0, to='elo_ladder.Player')),
                ('sender', models.ForeignKey(related_name=b'sender', default=0, to='elo_ladder.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
