# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_leaguevideo_thumbnail_second'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='relative_prefix',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
