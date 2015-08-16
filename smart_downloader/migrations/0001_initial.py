# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_url', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('provider_class', models.CharField(max_length=255, choices=[(b'smart_downloader.plugins.a3media.A3Media', b'A3Media')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('provider_name', models.CharField(max_length=255)),
                ('provider_url', models.URLField()),
                ('output_dir', models.CharField(max_length=255)),
                ('provider_class', models.CharField(max_length=255, choices=[(b'smart_downloader.plugins.a3media.A3Media', b'A3Media')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
