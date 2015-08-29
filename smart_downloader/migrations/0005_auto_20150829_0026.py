# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smart_downloader', '0004_auto_20150823_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='deleted_on',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='provider',
            field=models.ForeignKey(related_name=b'provider', blank=True, to='smart_downloader.Provider', null=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='task',
            field=models.ForeignKey(related_name=b'file_task', blank=True, to='djcelery.TaskMeta', null=True),
        ),
    ]
