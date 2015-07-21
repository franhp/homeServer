from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView

from random_video_downloader.models import Video, VideoDownloader


class VideoDownloaderView(TemplateView):
    template_name = 'random_video_downloader.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'downloads': Video.list_downloads(),
            'jobs': VideoDownloader.objects.all().exclude(
                name='Manual').order_by('-last_execution')
        })

    def post(self, request, *args, **kwargs):
        url = request.POST.get('add_url')
        title = request.POST.get('add_title')
        manual, _ = VideoDownloader.objects.get_or_create(name='Manual')
        Video.objects.create(video_url=url, title=title, provider=manual)
        return HttpResponseRedirect(reverse('downloader'))
