import importlib

from django.conf import settings

from django.db import models
from djcelery.models import TaskMeta

from tasks import download

import plugins


class ProviderNotFoundError(Exception):
    pass


def load_plugin(full_name):
    kls = full_name.split('.')[-1:][0]
    module_path = '.'.join(full_name.split('.')[:-1])
    return getattr(importlib.import_module(module_path), kls)


class File(models.Model):
    file_url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    provider = models.ForeignKey(
        'smart_downloader.Provider', null=True, blank=True,
        related_name='provider')
    task = models.ForeignKey(
        TaskMeta, related_name='file_task', null=True, blank=True)

    def __unicode__(self):
        return self.title

    def download(self):
        if self.provider and self.provider.provider_class:
            provider = load_plugin(self.provider.provider_class)()
            output_dir = self.provider.output_dir
        else:
            for kls, name in Provider.PROVIDERS:
                provider = load_plugin(kls)()
                if provider.match_pattern(self.file_url):
                    break
                provider = None
            if not provider:
                raise ProviderNotFoundError()
            output_dir = settings.DEFAULT_OUTPUT_DIR
        provider.download(url=self.file_url, output=output_dir)

    @property
    def percentage(self):
        return (self.downloaded_bytes * 100) / float(self.total_bytes)

    @property
    def total_bytes(self):
        return self.task.result.get('total')

    @property
    def downloaded_bytes(self):
        return self.task.result.get('current')


class Provider(models.Model):
    provider_name = models.CharField(max_length=255)
    provider_url = models.URLField()
    output_dir = models.CharField(max_length=255)

    PROVIDERS = [(x, x.split('.')[-1:][0]) for x in plugins.__all_plugins__]
    provider_class = models.CharField(choices=PROVIDERS, max_length=255)

    def __unicode__(self):
        return self.provider_name

    def find_more_links(self):
        assert self.provider_class is not None
        provider = load_plugin(self.provider_class)()
        outcome = provider.find_more_links(data=self)
        added = 0
        for result in outcome:
            name, link = result
            if not File.objects.filter(file_url=link).exists():
                added += 1
                download.apply_async(kwargs={
                    'url': link,
                    'name': name,
                    'provider': self,
                })
        return added
