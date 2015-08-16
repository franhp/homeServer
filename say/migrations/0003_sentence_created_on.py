# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('say', '0002_sentence_who'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentence',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 16, 23, 6, 5, 514614), auto_created=True),
            preserve_default=False,
        ),
    ]
