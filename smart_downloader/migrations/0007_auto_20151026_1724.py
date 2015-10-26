# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('smart_downloader', '0006_auto_20150905_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 26, 17, 24, 7, 506447), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='provider',
            name='provider_class',
            field=models.CharField(max_length=255, choices=[(b'smart_downloader.plugins.a3media.A3Media', b'A3Media'), (b'smart_downloader.plugins.chia.ChiaProvider', b'ChiaProvider'), (b'smart_downloader.plugins.transmission.TransmissionProvider', b'TransmissionProvider'), (b'smart_downloader.plugins.tube.ColouredTube', b'ColouredTube'), (b'smart_downloader.plugins.tv3alacarta.TV3Alacarta', b'TV3Alacarta'), (b'smart_downloader.plugins.default.DefaultProvider', b'DefaultProvider')]),
        ),
    ]
