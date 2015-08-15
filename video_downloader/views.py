from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView

from video_downloader.models import Video, VideoDownloader


class VideoDownloaderView(TemplateView):
    template_name = 'video_downloader.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'downloads': Video.list_downloads(),
            'jobs': VideoDownloader.objects.all().exclude(
                name='Manual').order_by('-last_execution')
        })

    def post(self, request, *args, **kwargs):
        url = request.POST.get('add_url')
        title = request.POST.get('add_title')
        restart = request.POST.get('restart')
        stop = request.POST.get('stop')
        mass = request.POST.get('mass')
        trigger = request.POST.get('trigger')

        manual, _ = VideoDownloader.objects.get_or_create(name='Manual')
        if url:
            t = title if title else url[-20:]
            Video.objects.create(video_url=url, title=t, provider=manual)
        elif mass:
            for url in mass.split():
                t = url[-20:]
                Video.objects.create(video_url=url, provider=manual, title=t)
        elif restart:
            Video.objects.filter(id=restart).update(status=Video.NOT_STARTED)
        elif stop:
            Video.objects.filter(id=stop).update(status=Video.FINISHED)
        elif trigger:
            VideoDownloader.objects.filter(id=trigger).update(force=True)

        return HttpResponseRedirect(reverse('downloader'))
