# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('rules', models.TextField(blank=True)),
                ('library_path', models.CharField(max_length=255, null=True, blank=True)),
                ('play_path', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LeagueVideo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('votes', models.IntegerField(default=0)),
                ('video_full_path', models.CharField(max_length=255)),
                ('video_rel_path', models.CharField(max_length=255)),
                ('league', models.ForeignKey(related_name=b'league', to='games.League')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
