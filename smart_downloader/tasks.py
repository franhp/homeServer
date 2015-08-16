from __future__ import absolute_import
from home.celery import app
from smart_downloader.models import File, Provider


@app.task
def download(file_id):
    f = File.objects.get(pk=file_id)
    f.download()


@app.task
def find_more_links(provider_id):
    f = Provider.objects.get(pk=provider_id)
    f.find_more_links()
