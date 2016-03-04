# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0005_league_relative_prefix'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaguevideo',
            name='video_rel_path',
        ),
    ]
