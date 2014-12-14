# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('elo_ladder', '0005_auto_20141105_0123'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResetPage',
            fields=[
                ('add_date', models.DateTimeField(verbose_name=b'date added')),
                ('code', models.TextField(serialize=False, primary_key=True)),
                ('used', models.BooleanField(default=0)),
                ('user', models.ForeignKey(default=0, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
