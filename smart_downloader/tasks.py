from __future__ import absolute_import
from celery import task


@task
def download(url=None, name=None, provider=None):
    from smart_downloader.models import File
    f, _ = File.objects.get_or_create(
        file_url=url, title=name, provider=provider)
    f.download()
    return 'Done!'


@task
def find_more_links(provider_id=None):
    from smart_downloader.models import Provider
    f = Provider.objects.get(pk=provider_id)
    return 'Added %s files' % f.find_more_links()
