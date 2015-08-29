from __future__ import absolute_import
from celery import task, current_task
from djcelery.models import TaskMeta


@task
def download(url=None, name=None, provider=None):
    from smart_downloader.models import File
    current_taskmeta = TaskMeta.objects.get(task_id=current_task.request.id)
    f = File.objects.get(file_url=url)
    f.title = f.find_title()
    f.task = current_taskmeta
    f.save()
    f.download()
    return 'Done!'


@task
def find_more_links(provider_id=None):
    from smart_downloader.models import Provider
    f = Provider.objects.get(pk=provider_id)
    return 'Added %s files' % f.find_more_links()
