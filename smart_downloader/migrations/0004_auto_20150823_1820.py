# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djcelery', '__first__'),
        ('smart_downloader', '0003_auto_20150823_1517'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='downloaded_bytes',
        ),
        migrations.RemoveField(
            model_name='file',
            name='total_bytes',
        ),
        migrations.AddField(
            model_name='file',
            name='task',
            field=models.ForeignKey(blank=True, to='djcelery.TaskMeta', null=True),
            preserve_default=True,
        ),
    ]
