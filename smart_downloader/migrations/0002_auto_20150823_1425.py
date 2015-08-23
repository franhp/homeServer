# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smart_downloader', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='downloaded_bytes',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='file',
            name='total_bytes',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
