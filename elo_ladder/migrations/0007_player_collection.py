# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elo_ladder', '0006_resetpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='collection',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
    ]
