# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaguevideo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 8, 22, 33, 48, 996198), auto_created=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='leaguevideo',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='leaguevideo',
            name='times_voted',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
