# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('video_url', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('status', models.IntegerField(default=0, choices=[(0, b'Queued'), (1, b'Started'), (2, b'Finished'), (3, b'Error')])),
                ('error', models.TextField(blank=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VideoDownloader',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('website', models.CharField(max_length=255, null=True, blank=True)),
                ('element_query', models.TextField(blank=True)),
                ('title_query', models.TextField(blank=True)),
                ('url_query', models.TextField(blank=True)),
                ('scheduled', models.BooleanField(default=False)),
                ('output_dir', models.CharField(default=b'~/Downloads', max_length=255)),
                ('last_execution', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='video',
            name='provider',
            field=models.ForeignKey(related_name=b'downloads', to='video_downloader.VideoDownloader'),
            preserve_default=True,
        ),
    ]
