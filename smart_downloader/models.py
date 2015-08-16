import inspect

from django.db import models

import plugins

PROVIDERS = [(x, x.split('.')[-1:][0]) for x in plugins.__all_plugins__]


class File(models.Model):
    file_url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    provider_class = models.CharField(choices=PROVIDERS, max_length=255)

    def __unicode__(self):
        return self.title

    def clean(self):
        if File.objects.filter(file_url=self.file_url).exists():
            raise Exception('Already downloaded!')

    def save(self, **kwargs):
        for kls in inspect.getmembers(plugins):
            if kls.match_pattern(self.file_url):
                self.provider_class = kls
            else:
                self.provider_class = 'DEFAULT'

        super(File, self).save(**kwargs)

    def download(self):
        provider = __import__(self.provider_class)
        return provider.download(self)

    @property
    def percentage(self):
        provider = __import__(self.provider_class)
        return provider.downloaded_bytes(self) / provider.total_bytes(self)


class Provider(models.Model):
    provider_name = models.CharField(max_length=255)
    provider_url = models.URLField()
    output_dir = models.CharField(max_length=255)
    provider_class = models.CharField(choices=PROVIDERS, max_length=255)

    def __unicode__(self):
        return self.provider_name

    def find_more_links(self):
        provider = __import__(self.provider_class)
        return provider.find_more_links()
