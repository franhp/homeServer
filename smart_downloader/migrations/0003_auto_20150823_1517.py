# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smart_downloader', '0002_auto_20150823_1425'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='provider_class',
        ),
        migrations.AddField(
            model_name='file',
            name='provider',
            field=models.ForeignKey(blank=True, to='smart_downloader.Provider', null=True),
            preserve_default=True,
        ),
    ]
