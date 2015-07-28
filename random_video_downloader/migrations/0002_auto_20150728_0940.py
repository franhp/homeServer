# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('random_video_downloader', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videodownloader',
            name='element_query',
        ),
        migrations.RemoveField(
            model_name='videodownloader',
            name='title_query',
        ),
        migrations.RemoveField(
            model_name='videodownloader',
            name='url_query',
        ),
        migrations.RemoveField(
            model_name='videodownloader',
            name='website',
        ),
        migrations.AddField(
            model_name='videodownloader',
            name='find_url_logic',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
