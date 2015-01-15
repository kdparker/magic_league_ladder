# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elo_ladder', '0008_tradeoffer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='collection',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='tradeoffer',
            name='offered_cards',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='tradeoffer',
            name='wanted_cards',
            field=models.TextField(default=b'', blank=True),
        ),
    ]
