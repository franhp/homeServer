# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('say', '0003_sentence_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentence',
            name='created_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
