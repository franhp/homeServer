# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_auto_20151108_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaguevideo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now, auto_created=True),
        ),
    ]
