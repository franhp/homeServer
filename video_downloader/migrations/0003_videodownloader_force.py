# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video_downloader', '0002_auto_20150728_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='videodownloader',
            name='force',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
