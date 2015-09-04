from celery.contrib.abortable import AbortableAsyncResult
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.views.generic.base import TemplateView
from tasks import download, find_more_links

from smart_downloader.models import Provider, File


class SmartDownloaderView(TemplateView):
    template_name = 'smart_downloader.html'

    def get_context_data(self, **kwargs):
        context = super(SmartDownloaderView, self).get_context_data(**kwargs)
        context['providers'] = Provider.objects.all()
        context['providerless'] = File.objects.filter(
            provider=None, deleted_on=None)
        return context

    def post(self, request, *args, **kwargs):
        retry = request.POST.get('retry')
        abort = request.POST.get('abort')
        archive = request.POST.get('archive')
        add = request.POST.get('add')
        trigger = request.POST.get('trigger_find_more_links')

        if add:
            for link in add.split('\n'):
                download.apply_async(kwargs={
                    'url': link
                })

        elif trigger:
            find_more_links.apply_async(kwargs={
                'provider_id': trigger
            })
        else:
            obj = File.objects.get(id=retry or abort or archive)

            if retry:
                download.apply_async(kwargs={
                    'url': obj.file_url,
                    'name': obj.title,
                    'provider': obj.provider,
                })
            elif abort:
                abortable = AbortableAsyncResult(
                    obj.task.task_id)
                abortable.abort()
            elif archive:
                obj.deleted_on = timezone.now()
                obj.save()

        return HttpResponseRedirect(reverse('smart-downloader'))
