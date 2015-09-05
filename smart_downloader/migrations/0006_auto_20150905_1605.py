# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smart_downloader', '0005_auto_20150829_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file_url',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='file',
            name='provider',
            field=models.ForeignKey(related_name=b'provider_files', blank=True, to='smart_downloader.Provider', null=True),
        ),
        migrations.AlterField(
            model_name='provider',
            name='provider_class',
            field=models.CharField(max_length=255, choices=[(b'smart_downloader.plugins.a3media.A3Media', b'A3Media'), (b'smart_downloader.plugins.chia.ChiaProvider', b'ChiaProvider'), (b'smart_downloader.plugins.transmission.TransmissionProvider', b'TransmissionProvider'), (b'smart_downloader.plugins.tube.ColouredTube', b'ColouredTube'), (b'smart_downloader.plugins.default.DefaultProvider', b'DefaultProvider')]),
        ),
    ]
