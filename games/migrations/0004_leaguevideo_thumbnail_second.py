# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_auto_20151108_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaguevideo',
            name='thumbnail_second',
            field=models.IntegerField(default=60),
            preserve_default=True,
        ),
    ]
